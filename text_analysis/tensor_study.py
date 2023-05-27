import torch
import torch.nn as nn


class selfAttention(nn.Module):
    def __init__(self, embed_size, heads):
        super(selfAttention, self).__init__()
        self.embed_size = embed_size  # d_model
        self.heads = heads  # h
        self.head_dim = embed_size // heads  # d_k

        assert (self.head_dim * heads ==
                embed_size), "Embed size needs to be divisible by heads"

        self.values = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.keys = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.queries = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.fc_out = nn.Linear(heads*self.head_dim, embed_size)

    def forward(self, values, keys, query, mask):
        N = query.shape[0]
        value_len, key_len, query_len = values.shape[1], keys.shape[1], query.shape[1]

        # Split embedding into self.heads pieces
        values = values.reshape(N, value_len, self.heads, self.head_dim)
        keys = keys.reshape(N, key_len, self.heads, self.head_dim)
        query = query.reshape(N, query_len, self.heads, self.head_dim)

        values = self.values(values)  # (N, value_len, heads, head_dim)
        keys = self.keys(keys)  # (N, key_len, heads, head_dim)
        query = self.queries(query)  # (N, query_len, heads, head_dim)
        
        energy = torch.einsum("nqhd,nkhd->nhqk", [query, keys])
        '''
        Explanation of einsum:
        - nqhd: (N, query_len, heads, head_dim)
        - nkhd: (N, key_len, heads, head_dim)
        - nhqk: (N, heads, query_len, key_len)
        nqhd * nkhd = nhqk'''
        # query shape: (N, query_len, heads, head_dim)
        # keys shape: (N, key_len, heads, head_dim)
        # energy shape: (N, heads, query_len, key_len)
        # being N the batch size, query_len the length of the query, key_len the length of the key
        if mask is not None:
            energy = energy.masked_fill(mask == 0, float("-1e20"))
            # if mas == 0 then energy = -1e20

        attention = torch.softmax(energy/(self.embed_size**(1/2)), dim=3)

        out = torch.einsum("nhql,nlhd->nqhd", [attention, values]).reshape(
            N, query_len, self.heads*self.head_dim
        )
        # attention shape: (N, heads, query_len, key_len)
        # values shape: (N, value_len, heads, head_dim)
        # out shape: (N, query_len, heads, head_dim)
        # being N the batch size, query_len the length of the query, key_len the length of the key

        # reshape is needed to concatenate the heads
        out = self.fc_out(out)
        # out shape: (N, query_len, embed_size)
        return out


class TransformerBlock(nn.Module):
    '''
    Transformer Block is composed by:
    - Multi-head attention
    - Layer Normalization
    - Feed Forward
    - Dropout
    It is common between the encoder and the decoder'''
    def __init__(self, embed_size, heads, dropout, forward_expansion):
        super(TransformerBlock, self).__init__()
        self.attention = selfAttention(embed_size, heads)
        self.norm1 = nn.LayerNorm(embed_size)
        self.norm2 = nn.LayerNorm(embed_size)

        self.feed_forward = nn.Sequential(
            nn.Linear(embed_size, forward_expansion*embed_size),
            nn.ReLU(),
            nn.Linear(forward_expansion*embed_size, embed_size)
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, value, key, query, mask):
        attention = self.attention(value, key, query, mask)
        x = self.dropout(self.norm1(attention + query))
        forward = self.feed_forward(x)
        out = self.dropout(self.norm2(forward + x))
        return out


class Encoder(nn.Module):
    def __init__(self,
                 src_vocab_size,
                 embed_size,
                 num_layers,
                 heads,
                 device,
                 forward_expansion,
                 dropout,
                 max_length):
        '''
        src_vocab_size: size of the vocabulary of the source language
        embed_size: size of the embedding
        num_layers: number of layers of the encoder
        heads: number of heads of the self-attention
        device: device to use
        forward_expansion: factor to multiply the embedding size in the feed forward
        dropout: dropout rate
        max_length: maximum length of the sentence'''

        super(Encoder, self).__init__()
        self.embed_size = embed_size
        self.device = device
        self.word_embedding = nn.Embedding(src_vocab_size, embed_size)
        self.position_embedding = nn.Embedding(max_length, embed_size)
        self.layers = nn.ModuleList(
            [TransformerBlock(embed_size, heads, dropout, forward_expansion)
             for _ in range(num_layers)]
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask):

        N, seq_length = x.shape
        positions = torch.arange(0, seq_length).expand(
            N, seq_length).to(self.device)
        #arrange creates a tensor with the numbers from 0 to seq_length
        #expand creates a tensor with the same shape as x, but with the numbers from 0 to seq_length
        #to(device) moves the tensor to the device -> the device is the GPU if available, otherwise the CPU

        out = self.dropout(self.word_embedding(
            x) + self.position_embedding(positions))
        # out shape: (N, seq_length, embed_size)
        for layer in self.layers:
            out = layer(out, out, out, mask)
        return out

class DecoderBlock(nn.Module):
    def __init__(self, embed_size, heads, forward_expansion, dropout, device) -> None:
        super(DecoderBlock, self).__init__()
        self.attention = selfAttention(embed_size, heads)
        self.norm = nn.LayerNorm(embed_size)
        self.transformer_block = TransformerBlock(
            embed_size, heads, dropout, forward_expansion)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, value, key, src_mask, trg_mask):
        '''
        x: input
        value: output of the encoder
        key: output of the encoder
        src_mask: mask for the encoder
        trg_mask: mask for the decoder'''

        attention = self.attention(x, x, x, trg_mask)
        query = self.dropout(self.norm(attention + x))
        out = self.transformer_block(value, key, query, src_mask)
        return out

class Decoder(nn.Module):
    def __init__(self,
                 trg_vocab_size,
                 embed_size,
                 num_layers,
                 heads,
                 forward_expansion,
                 dropout,
                 device,
                 max_length):
        super(Decoder, self).__init__()
        self.device = device
        self.word_embedding = nn.Embedding(trg_vocab_size, embed_size)
        self.position_embedding = nn.Embedding(max_length, embed_size)
        self.layers = nn.ModuleList(
            [DecoderBlock(embed_size, heads, forward_expansion, dropout, device)
             for _ in range(num_layers)]
        )
        self.fc_out = nn.Linear(embed_size, trg_vocab_size)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, enc_out, src_mask, trg_mask):
        N, seq_length = x.shape
        positions = torch.arange(0, seq_length).expand(
            N, seq_length).to(self.device)
        
        #arrange creates a tensor with the numbers from 0 to seq_length
        #expand creates a tensor with the same shape as x, but with the numbers from 0 to seq_length
        #to(device) moves the tensor to the device -> the device is the GPU if available, otherwise the CPU

        x = self.dropout(self.word_embedding(
            x) + self.position_embedding(positions))
        for layer in self.layers:
            x = layer(x, enc_out, enc_out, src_mask, trg_mask)
        out = self.fc_out(x)
        return out

class Transformer(nn.Module):
    def __init__(
            self,
            src_vocab_size,
            trg_vocab_size,
            src_pad_idx,
            trg_pad_idx,
            embed_size=256,
            num_layers=6,
            forward_expansion=4,
            heads=8,
            dropout=0,
            device="cuda",
            max_length=100
    ):
        super(Transformer, self).__init__()
        self.encoder = Encoder(src_vocab_size,
                               embed_size,
                               num_layers,
                               heads,
                               device,
                               forward_expansion,
                               dropout,
                               max_length)
        self.decoder = Decoder(trg_vocab_size,
                               embed_size,
                               num_layers,
                               heads,
                               forward_expansion,
                               dropout,
                               device,
                               max_length)
        self.src_pad_idx = src_pad_idx
        self.trg_pad_idx = trg_pad_idx
        self.device = device
    
    def make_src_mask(self, src):
        src_mask = (src != self.src_pad_idx).unsqueeze(1).unsqueeze(2)
        #src_mask shape: (N, 1, 1, src_len)
        #(src != self.src_pad_idx) returns a tensor with the same shape as src, but with True where src != self.src_pad_idx and False otherwise
        #unsqueeze(1) adds a dimension at index 1
        #unsqueeze(2) adds a dimension at index 2
        return src_mask.to(self.device)
    
    def make_trg_mask(self, trg):
        N, trg_len = trg.shape
        trg_mask = torch.tril(torch.ones((trg_len, trg_len))).expand(
            N, 1, trg_len, trg_len)
        #trg_mask shape: (N, 1, trg_len, trg_len), 1 refers to the dimension of the head
        # torch.tril returns the lower triangular part of a matrix of size trg_len x trg_len including the diagonal
        # expand creates a tensor with the same shape as trg, but with the lower triangular part of a matrix
        return trg_mask.to(self.device)
    
    def forward(self, src, trg):
        src_mask = self.make_src_mask(src)
        trg_mask = self.make_trg_mask(trg)
        enc_src = self.encoder(src, src_mask)
        out = self.decoder(trg, enc_src, src_mask, trg_mask)
        return out

if __name__ == "__main__":
    # Test main
    device = torch.device("mps" if torch.cuda.is_available() else "cpu")
    print(device)
    x = torch.tensor([[1, 5, 6, 4, 3, 9, 5, 2, 0],
                      [1, 8, 7, 3, 4, 5, 6, 7, 2]]).to(device)
    trg = torch.tensor([[1, 7, 4, 3, 5, 9, 2, 0],
                        [1, 5, 6, 2, 4, 7, 6, 2]]).to(device)
    src_pad_idx = 0
    trg_pad_idx = 0
    src_vocab_size = 10
    trg_vocab_size = 10
    model = Transformer(src_vocab_size, trg_vocab_size, src_pad_idx, trg_pad_idx, device=device).to(device)
    out = model(x, trg[:, :-1])
    print(out.shape)

'''
In our case we won't need all the transformer architecture, because we are not translating from one language to another, but we are just classifying a corpus, wethere it is male or female.
So we will use only the encoder part of the transformer.
Leaving to future work the possibility to modify the model architecture
'''
# TODO give it a look on how to apply the positional encoding
# TODO read the pytorch implementation of the transformer