# Machine Learning 101 : Multi Linear Regression

## Prerequisites

Understanding of [Simple Linear Regression][].  


## Multi linear regression  

It follows the formula  `result = bias + slope1 * feature1 + slope2 * feature2 + ... + + slopeN * featureN`



### Dummy  Variable trap
Rule of thumb : one variable less than the count


Should not use all features but use only use select the right Features
Garbage in = Garbage out
Too much complexity
[Simple Linear Regression]:Simple%20Linear%20Regression.md

### Methods
All - In
    Use all variables,  you know what the main variables, Have prior knowledge, Have to or forced to or planning for Backward elimination 
Step wise regression
    Backward eliminition (fastest)
        
    Forward selection
    Bidirectional eliminiation (default implied as stepwise regression)
All Possible Models (Score comparison)