
from . import PedalBoardAudiomentation
from pedalboard import Pedalboard, Compressor
from typing import Optional
from torch import Tensor


class CompressorAudiomentation(PedalBoardAudiomentation):
    
    
    
    def __init__(self, board=None, sample_rate = 22050, mode='per_example', p=0.5, p_mode=None, output_type=None,randomize_parameters = True, makeup_gain = False,*args, **kwargs):
        
        try:
            board = Pedalboard([
                Compressor(**kwargs)
            ])
        except:
            board = Pedalboard([
                Compressor()
            ])
        
        super().__init__(board, mode, p, p_mode, sample_rate, output_type=output_type, randomize_parameters=randomize_parameters)
        
        self.makeup_gain = makeup_gain
        self.set_kwargs(**kwargs)
        
    def __call__(self, samples: Tensor, sample_rate: int, targets: Optional[Tensor] = None, target_rate: Optional[int] = None):
        ## get the maxes and mins of the samples along the channel axis
        if self.makeup_gain:
            norm_maxes = samples.max(dim=1, keepdim=True)[0]
        out_ =  self.forward(samples, sample_rate, targets, target_rate)
        if self.makeup_gain:
            samples = out_.samples
            # normalize to the same maxes
            new_maxes = samples.max(dim=1, keepdim=True)[0]
            samples = samples * norm_maxes/new_maxes
            new_maxes = samples.max(dim=1, keepdim=True)[0]
            assert (new_maxes - norm_maxes).abs().max() < 1e-6
            out_.samples = samples
            
        return out_
    