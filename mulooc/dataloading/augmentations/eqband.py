
from . import PedalBoardAudiomentation, MultiPedalBoardAudiomentation
from pedalboard import Pedalboard, PeakFilter, HighpassFilter, LowpassFilter, HighShelfFilter, LowShelfFilter


class HighPassAudioMentation(PedalBoardAudiomentation):
    
    def __init__(self, board=None, sample_rate = 22050, mode='per_example', p=0.5, p_mode=None, output_type=None,randomize_parameters = True, *args, **kwargs):
        
        try:
            board = Pedalboard([
                HighpassFilter(**kwargs)
            ])
        except:
            board = Pedalboard([
                HighpassFilter()
            ])
        
        print(board)
        super().__init__(board, mode, p, p_mode, sample_rate, output_type=output_type, randomize_parameters=randomize_parameters)
        # print(self.output_type)
        
        self.set_kwargs(**kwargs)
        
class LowPassAudioMentation(PedalBoardAudiomentation):
        
        def __init__(self, board=None, sample_rate = 22050, mode='per_example', p=0.5, p_mode=None, output_type=None,randomize_parameters = True, *args, **kwargs):
            
            try:
                board = Pedalboard([
                    LowpassFilter(**kwargs)
                ])
            except:
                board = Pedalboard([
                    LowpassFilter()
                ])
            
            print(board)
            super().__init__(board, mode, p, p_mode, sample_rate, output_type=output_type, randomize_parameters=randomize_parameters)
            # print(self.output_type)
            
            self.set_kwargs(**kwargs)

class HighShelfAudioMentation(PedalBoardAudiomentation):
        
        def __init__(self, board=None, sample_rate = 22050, mode='per_example', p=0.5, p_mode=None, output_type=None,randomize_parameters = True, *args, **kwargs):
            
            try:
                board = Pedalboard([
                    HighShelfFilter(**kwargs)
                ])
            except:
                board = Pedalboard([
                    HighShelfFilter()
                ])
            
            print(board)
            super().__init__(board, mode, p, p_mode, sample_rate, output_type=output_type, randomize_parameters=randomize_parameters)
            # print(self.output_type)
            
            self.set_kwargs(**kwargs)
            

class LowShelfAudioMentation(PedalBoardAudiomentation):
            
            def __init__(self, board=None, sample_rate = 22050, mode='per_example', p=0.5, p_mode=None, output_type=None,randomize_parameters = True, *args, **kwargs):
                
                try:
                    board = Pedalboard([
                        LowShelfFilter(**kwargs)
                    ])
                except:
                    board = Pedalboard([
                        LowShelfFilter()
                    ])
                
                print(board)
                super().__init__(board, mode, p, p_mode, sample_rate, output_type=output_type, randomize_parameters=randomize_parameters)
                # print(self.output_type)
                
                self.set_kwargs(**kwargs)
                
                
class BandAudioMentation(PedalBoardAudiomentation):
    
    def __init__(self, board=None, sample_rate = 22050, mode='per_example', p=0.5, p_mode=None, output_type=None,randomize_parameters = True, *args, **kwargs):
        
        try:
            board = Pedalboard([
                PeakFilter(**kwargs)
            ])
        except:
            board = Pedalboard([
                PeakFilter()
            ])
        
        print(board)
        super().__init__(board, mode, p, p_mode, sample_rate, output_type=output_type, randomize_parameters=randomize_parameters)
        # print(self.output_type)
        
        self.set_kwargs(**kwargs)
    

class EQ8Band(MultiPedalBoardAudiomentation):
    
    def __init__(self, board=None, sample_rate = 22050, mode='per_example', p=0.5, p_mode=None, output_type=None, randomize_parameters = True, *args, **kwargs):
        
        highpasskwargs = kwargs.get('highpass', {})
        lowpasskwargs = kwargs.get('lowpass', {})
        highshelfkwargs = kwargs.get('highshelf', {})
        lowshelfkwargs = kwargs.get('lowshelf', {})
        band1kwargs = kwargs.get('band1', {})
        band2kwargs = kwargs.get('band2', {})
        band3kwargs = kwargs.get('band3', {})
        band4kwargs = kwargs.get('band4', {})
        band5kwargs = kwargs.get('band5', {})
        band6kwargs = kwargs.get('band6', {})
        
        board = [
            HighPassAudioMentation(**highpasskwargs),
            LowPassAudioMentation(**lowpasskwargs),
            HighShelfAudioMentation(**highshelfkwargs),
            LowShelfAudioMentation(**lowshelfkwargs),
            BandAudioMentation(**band1kwargs),
            BandAudioMentation(**band2kwargs),
            BandAudioMentation(**band3kwargs),
            BandAudioMentation(**band4kwargs),
            BandAudioMentation(**band5kwargs),
            BandAudioMentation(**band6kwargs)
        ]
        
        board[0].set_name('HighPass')
        board[1].set_name('LowPass')
        board[2].set_name('HighShelf')
        board[3].set_name('LowShelf')
        board[4].set_name('Band1')
        board[5].set_name('Band2')
        board[6].set_name('Band3')
        board[7].set_name('Band4')
        board[8].set_name('Band5')
        board[9].set_name('Band6')
        
    
    
        
        super().__init__(board, mode, p, p_mode, sample_rate , output_type=output_type, randomize_parameters=randomize_parameters)
        