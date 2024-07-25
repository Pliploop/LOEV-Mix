


from typing import Optional
import torch
from torch_audiomentations.core.transforms_interface import BaseWaveformTransform
from torch_audiomentations.utils.object_dict import ObjectDict
from torch import Tensor
import numpy as np



class PedalBoardAudiomentation(BaseWaveformTransform):
    """
    A wrapper for pedalboard, a python package for audio effects.
    Callable, and can be used as a torch transform.
    """
    
    
    supported_modes = {"per_example"}

    supports_multichannel = True
    requires_sample_rate = True

    supports_target = True
    requires_target = False

    
    def __init__(self, board,
                  mode: str = "per_example",
        p: float = 0.5,
        p_mode: str = None,
        sample_rate: int = None,
        target_rate: int = None,
        output_type: Optional[str] = 'dict',
        randomize_parameters: bool = True,
        name = ''):
        super().__init__(
            mode=mode,
            p=p,
            p_mode=p_mode,
            sample_rate=sample_rate,
            target_rate=target_rate,
            output_type=output_type,
        )
        """
        :param board: Pedalboard object: Pedalboard object to be used for audio processing
        :param sample_rate:
        :param mode: ``per_example``, ``per_channel``, or ``per_batch``. Default ``per_example``.
        :param p:
        :param p_mode:
        :param target_rate:
        
        """
        self._randomize_parameters = randomize_parameters
        if self.mode not in self.supported_modes:
            raise ValueError(
                f"Invalid mode: {self.mode}. Supported modes are: {self.supported_modes}"
            )
        
        self._board = board
        self._sample_rate = sample_rate
        self._mode = mode
        self._p = p 
        self._name = name

        
        self.transform_parameters = {}
        self.transform_ranges = {}
        
    # indexing with [] should return self._board[index]
    def __getitem__(self, index):
        return self._board[index]
    
    def append(self, effect):
        self._board.append(effect)
    
    # def __call__(self, samples):
    #     return self.process(samples)
    
    def process(self, samples):
        ## audio is of shape [Batch, channels, time], as expected by pedalboard
        new_audio = []
        for i in range(samples.shape[0]):
            input_ = samples[i,:,:].numpy()
            effected = self._board(input_array = input_, sample_rate = self._sample_rate)
            new_audio.append(torch.tensor(effected).unsqueeze(0))
        
        
        return torch.cat(new_audio, dim=0)

    def apply_transform(
        
        self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,
    ) -> ObjectDict:
        
        batch_size, num_channels, num_samples = samples.shape
        
        for i in range(batch_size):
            if self._randomize_parameters:
                for key in self.transform_parameters:   
                    self._board[0].__setattr__(key, self.transform_parameters[key][i]) if key!="should_apply" else None
            samples[i, ...] = self.process(samples[i][None])
        
        
        return ObjectDict(
            samples=samples,
            sample_rate=sample_rate,
            targets=targets,
            target_rate=target_rate,
            should_apply = self.transform_parameters["should_apply"]
        )    

    def set_kwargs(self, **kwargs):
        
        # kwargs is a dictionary of parameters.
        # each key can be either "max_parameter", "min_parameter"
        # if there is a max, there cannot not be a min for the same parameter.
        # if both exist then set the range in transform ranges
        # if only one exists, get the current value of the parameter and set the range to be [min_value, max_value] according to the parameter.
        
        for key in kwargs:
            if "max" in key:
                parameter_name = key.replace("max_", "")
                if "min_" + parameter_name in kwargs:
                    self.transform_ranges[parameter_name] = [kwargs["min_" + parameter_name], kwargs[key]]
                else:
                    current = eval(f"self._board[0].{parameter_name}")
                    if current > kwargs[key]:
                        self.transform_ranges[parameter_name] = [kwargs[key], current]
                    else:
                        self.transform_ranges[parameter_name] = [current, kwargs[key]]
            elif "min" in key:
                parameter_name = key.replace("min_", "")
                if "max_" + parameter_name in kwargs:
                    self.transform_ranges[parameter_name] = [kwargs[key], kwargs["max_" + parameter_name]]
                else:
                    current = eval(f"self._board[0].{parameter_name}")
                    if current < kwargs[key]:
                        self.transform_ranges[parameter_name] = [kwargs[key], current]
                    else:
                        self.transform_ranges[parameter_name] = [current, kwargs[key]]
            else:
                self._board[0].__setattr__(key, kwargs[key])
                
        if len(self.transform_ranges) == 0:
            self._randomize_parameters = False
        
    def randomize_parameters(self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,):
        
        
        batch_size, num_channels, num_samples = samples.shape
        
        
        if self._randomize_parameters:
            if self._mode == "per_example":
                for key in self.transform_ranges:
                    self.transform_parameters[key] = list(np.random.uniform(self.transform_ranges[key][0], self.transform_ranges[key][1], batch_size))
                        
            elif self._mode == "per_batch":
                for key in self.transform_ranges:
                    self.transform_parameters[key] = [np.random.uniform(self.transform_ranges[key][0], self.transform_ranges[key][1])] * batch_size
            
                    
        # print(self.transform_parameters)
    
    def set_name(self, name):
        self._name = name
        
class MultiPedalBoardAudiomentation(BaseWaveformTransform):
    """
    A wrapper for pedalboard, a python package for audio effects.
    Callable, and can be used as a torch transform.
    """
    
    
    supported_modes = {"per_example"}

    supports_multichannel = True
    requires_sample_rate = True

    supports_target = True
    requires_target = False

    
    def __init__(self, boards,
                  mode: str = "per_example",
        p: float = 0.5,
        p_mode: str = None,
        sample_rate: int = None,
        target_rate: int = None,
        output_type: Optional[str] = 'dict',
        randomize_parameters: bool = True,):
        super().__init__(
            mode=mode,
            p=p,
            p_mode=p_mode,
            sample_rate=sample_rate,
            target_rate=target_rate,
            output_type=output_type,
        )
        """
        :param board: Pedalboard object: Pedalboard object to be used for audio processing
        :param sample_rate:
        :param mode: ``per_example``, ``per_channel``, or ``per_batch``. Default ``per_example``.
        :param p:
        :param p_mode:
        :param target_rate:
        
        """
        self._randomize_parameters = randomize_parameters
        if self.mode not in self.supported_modes:
            raise ValueError(
                f"Invalid mode: {self.mode}. Supported modes are: {self.supported_modes}"
            )
        
    
        self._boards = boards
        self._sample_rate = sample_rate
        self._mode = mode
        self._p = p

        
        self.transform_parameters = {}
        self.transform_ranges = {}
        
    # indexing with [] should return self._board[index]
    
    # def __call__(self, samples):
    #     return self.process(samples)
    
    
    def apply_transform(
        
        self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,
    ) -> ObjectDict:
        
        batch_size, num_channels, num_samples = samples.shape
        
        
        for board in self._boards:
            samples = board(samples)
        
        return ObjectDict(
            samples=samples,
            sample_rate=sample_rate,
            targets=targets,
            target_rate=target_rate,
            # should_apply = self.transform_parameters["should_apply"]
        )
        
        
    def set_kwargs(self, kwargs):
        for k in range(len(kwargs)):
            kwarg = kwargs[k]
            self._boards[k].set_kwargs(**kwarg)
            
            self.transform_ranges.update(self._boards[k].transform_ranges)
            
    def randomize_parameters(self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,):
        
        for board in self._boards:
            board.randomize_parameters(samples, sample_rate, targets, target_rate)
        
    def __call__(self, samples: Tensor, sample_rate: int, targets: Optional[Tensor] = None, target_rate: Optional[int] = None) -> ObjectDict:
        out_ =  self.forward(samples, sample_rate, targets, target_rate)
        
        # should_apply = []
        for board in self._boards:
            # should_apply.append(board.transform_parameters["should_apply"])
            board_tfms = board.transform_parameters
            # change the keys to the names
            board_tfms = {board._name + "_" + key: board_tfms[key] for key in board_tfms}
            self.transform_parameters.update(board_tfms)
            
        # global_should_apply = [any(t) for t in zip(*should_apply)]
        # self.transform_parameters["should_apply"] = torch.tensor(global_should_apply)
        
        return out_