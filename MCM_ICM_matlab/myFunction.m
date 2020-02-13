function R=myFunction(X)
[V,D] = eig(X);
R = V*diag(exp(diag(D)))/V;
