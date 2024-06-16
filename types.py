from typing import Iterable,Union,Callable,Dict,Optional,Tuple,Any 
from torch import Tensor 

Params=Union[Iterable[Tensor],Iterable[dict]]

LossClousure=Callable[[],float]
OptLossClousre=Optional[LossClousure]
Betas2=Tuple[float,float]
State=Dict[str,Any]
OptFloat=Optional[float]


