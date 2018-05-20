# Machine Learning 101 : Simple Linear Regression

## A Simple linear regression  
It follows the formula  `result = bias + slope * feature`  

Which indicates that `bias` is a point on `feature` to `result` graph, when `feature` is `zero`. This also means that bias is an intersection on the result for feature is zero.  

`slope` decides the amount of variation that can be observed **per unit** change of `feature` to corresponding **per unit** change of `result`  

### Use cases where linear regression can be used  
    It can be used any where the `feature` set increases or decreases with the `result` set, with some kind of slope.


`Sum(Observed Result - Predicted Result)^2`  should be minimum for all `features` 

## Steps
The preprocessing steps would be:
+ Since we are dealing with features that are infact related to each other comparatively, we do not need to do feature scaling.  