from torch_audiomentations.core.transforms_interface import BaseWaveformTransform
from torch_audiomentations.utils.object_dict import ObjectDict

from torch import Tensor
from typing import Optional
import librosa
import numpy as np
import torch



    
       
       
class Width(BaseWaveformTransform):
    
    supported_modes = {"per_batch", "per_example", "per_channel"}

    supports_multichannel = True
    requires_sample_rate = True

    supports_target = True
    requires_target = False

    def __init__(
        self,
        max_width: float = 1.0,
        min_width: float = 0.0,
        mode: str = "per_example",
        p: float = 0.5,
        p_mode: str = None,
        sample_rate: int = None,
        target_rate: int = None,
        output_type: Optional[str] = None,
        ):

        super().__init__(
            mode=mode,
            p=p,
            p_mode=p_mode,
            sample_rate=sample_rate,
            target_rate=target_rate,
            output_type=output_type,
        )

        if min_width > max_width:
            raise ValueError("max_width must be > min_width")
        if not sample_rate:
            raise ValueError("sample_rate is invalid.")
        self._sample_rate = sample_rate
        self._max_width = max_width
        self._min_width = min_width
        self._mode = mode

    def randomize_parameters(
        self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,
    ):
        """
        :param samples: (batch_size, num_channels, num_samples)
        :param sample_rate:
        """
        batch_size, num_channels, num_samples = samples.shape

        if self._mode == "per_example":
            # uniformsampling
            self.transform_parameters['widths'] = list(np.random.uniform(self._min_width, self._max_width, batch_size))
        
        elif self._mode == "per_batch":
            self.transform_parameters['widths'] = [np.random.uniform(self._min_width, self._max_width)] * batch_size
            
    def apply_transform(
        
        self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,
    ) -> ObjectDict:
        """
        :param samples: (batch_size, num_channels, num_samples)
        :param sample_rate:
        """
        batch_size, num_channels, num_samples = samples.shape

        if sample_rate is not None and sample_rate != self._sample_rate:
            raise ValueError(
                "sample_rate must match the value of sample_rate "
                + "passed into the TimeStretch constructor"
            )
        sample_rate = self.sample_rate

        if self._mode == "per_example":
            for i in range(batch_size):
                samples[i, ...] = self.widen(
                    samples[i][None],
                    self.transform_parameters["widths"][i],
                    sample_rate,
                )[0]


        elif self._mode == "per_batch":
            samples = self.widen(
                samples, 
                self.transform_parameters["widths"][0],
                sample_rate
            )


        return ObjectDict(
            samples=samples,
            sample_rate=sample_rate,
            targets=targets,
            target_rate=target_rate,
        )
        
    def widen(self,samples: Tensor, width = 1, sr = 22050) -> Tensor:
        
       # time stretch the signal and truncate to the original length
        
        
        width = 2 * np.clip(width,0,1)
        
        L = samples[:,0,:]
        R = samples[:,1,:]
        
        M = (L+R)/(2**0.5)
        S = (L-R)/(2**0.5)
        
        M *= (2-width)**0.5
        S *= width**0.5
        
        L = (M+S)/(2**0.5)
        R = (M-S)/(2**0.5)
        
        return torch.stack([L,R],dim = 1)
        

class Pan(BaseWaveformTransform):
    
    supported_modes = {"per_batch", "per_example", "per_channel"}

    supports_multichannel = True
    requires_sample_rate = True

    supports_target = True
    requires_target = False

    def __init__(
        self,
        max_pan: float = 1.0,
        min_pan: float = -1.0,
        mode: str = "per_example",
        p: float = 0.5,
        p_mode: str = None,
        sample_rate: int = None,
        target_rate: int = None,
        output_type: Optional[str] = None,
        ):
        
        super().__init__(
            mode=mode,
            p=p,
            p_mode=p_mode,
            sample_rate=sample_rate,
            target_rate=target_rate,
            output_type=output_type,
        )

        if min_pan > max_pan:
            raise ValueError("max_pan must be > min_pan")
        if not sample_rate:
            raise ValueError("sample_rate is invalid.")
        self._sample_rate = sample_rate
        self._max_pan = max_pan
        self._min_pan = min_pan
        self._mode = mode

    def randomize_parameters(
        self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,
    ):
        """
        :param samples: (batch_size, num_channels, num_samples)
        :param sample_rate:
        """
        batch_size, num_channels, num_samples = samples.shape

        if self._mode == "per_example":
            # uniformsampling
            self.transform_parameters['pans'] = list(np.random.uniform(self._min_pan, self._max_pan, batch_size))
        
        elif self._mode == "per_batch":
            self.transform_parameters['pans'] = [np.random.uniform(self._min_pan, self._max_pan)] * batch_size
    
    def apply_transform(
        
        self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,
    ) -> ObjectDict:
        """
        :param samples: (batch_size, num_channels, num_samples)
        :param sample_rate:
        """
        batch_size, num_channels, num_samples = samples.shape

        if sample_rate is not None and sample_rate != self._sample_rate:
            raise ValueError(
                "sample_rate must match the value of sample_rate "
                + "passed into the TimeStretch constructor"
            )
        sample_rate = self.sample_rate

        if self._mode == "per_example":
            for i in range(batch_size):
                samples[i, ...] = self.pan(
                    samples[i][None],
                    self.transform_parameters["pans"][i],
                    sample_rate,
                )[0]


        elif self._mode == "per_batch":
            samples = self.pan(
                samples, 
                self.transform_parameters["pans"][0],
                sample_rate
            )

        return ObjectDict(
            samples=samples,
            sample_rate=sample_rate,
            targets=targets,
            target_rate=target_rate,
        )
        
    def pan(self,samples: Tensor, angle = 0, sr = 22050) -> Tensor:
        
        L = samples[:,0,:]
        R = samples[:,1,:]
        
        angle = np.clip(angle,-1,1) / 2 + 1/2
        
        L = L * np.cos(angle * np.pi/2)
        R = R * np.sin(angle * np.pi/2)
        
        return torch.stack([L,R],dim = 1)
    

#class that combines both
class Stereo(BaseWaveformTransform):
    
    supported_modes = {"per_batch", "per_example", "per_channel"}

    supports_multichannel = True
    requires_sample_rate = True

    supports_target = True
    requires_target = False

    def __init__(
        self,
        max_pan: float = 1.0,
        min_pan: float = -1.0,
        max_width: float = 1.0,
        min_width: float = 0.0,
        mode: str = "per_example",
        p: float = 0.5,
        p_mode: str = None,
        sample_rate: int = None,
        target_rate: int = None,
        output_type: Optional[str] = None,
        ):

        super().__init__(
            mode=mode,
            p=p,
            p_mode=p_mode,
            sample_rate=sample_rate,
            target_rate=target_rate,
            output_type=output_type,
        )

        if min_pan > max_pan:
            raise ValueError("max_pan must be > min_pan")
        if not sample_rate:
            raise ValueError("sample_rate is invalid.")
        self.pan = Pan(max_pan = max_pan, min_pan = min_pan, mode = mode, p = 1, p_mode = p_mode, sample_rate = sample_rate, target_rate = target_rate, output_type = output_type)
        self.width = Width(max_width = max_width, min_width = min_width, mode = mode, p = 1, p_mode = p_mode, sample_rate = sample_rate, target_rate = target_rate, output_type = output_type)
        
    def randomize_parameters(
        self,
        samples: Tensor = None,
        sample_rate: Optional[int] = None,
        targets: Optional[Tensor] = None,
        target_rate: Optional[int] = None,
    ):
        """
        :param samples: (batch_size, num_channels, num_samples)
        :param sample_rate:
        """
        self.pan.randomize_parameters(samples, sample_rate, targets, target_rate)
        self.width.randomize_parameters(samples, sample_rate, targets, target_rate)
        
        
    def apply_transform(
            
            self,
            samples: Tensor = None,
            sample_rate: Optional[int] = None,
            targets: Optional[Tensor] = None,
            target_rate: Optional[int] = None,
        ) -> ObjectDict:
            """
            :param samples: (batch_size, num_channels, num_samples)
            :param sample_rate:
            """
            
            
            
            samples = self.pan(samples, sample_rate, targets, target_rate)
            samples = self.width(samples, sample_rate, targets, target_rate)
            if 'pans' in self.pan.transform_parameters:
                self.transform_parameters['pans'] = self.pan.transform_parameters.get('pans', None)
            if 'widths' in self.width.transform_parameters:
                self.transform_parameters['widths'] = self.width.transform_parameters.get('widths', None)
            
    
            return ObjectDict(
                samples=samples,
                sample_rate=sample_rate,
                targets=targets,
                target_rate=target_rate,
            )
            
    def __call__(self, samples: Tensor, sample_rate: int, targets: Optional[Tensor] = None, target_rate: Optional[int] = None) -> ObjectDict:
        out_ =  self.forward(samples, sample_rate, targets, target_rate)
        # self.transform_parameters['should_apply'] = torch.tensor([any(t) for t in zip(self.pan.transform_parameters['should_apply'], self.width.transform_parameters['should_apply'])])
        
        # print(self.transform_parameters)
        # print(self.pan.transform_parameters)
        # print(self.width.transform_parameters)
        
        return out_