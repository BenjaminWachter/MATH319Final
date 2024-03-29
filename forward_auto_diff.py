#!/usr/bin/python3

import math

pi = math.pi
e = math.e

class Var: # Contains 
    def __init__(self, val, der):
        self.val = val
        self.der = der
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Var(self.val+other.val, self.der+other.der)
        else:
            return Var(self.val+other, self.der)
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Var(self.val*other.val, self.der*other.val+self.val*other.der)
        else:
            return Var(self.val*other, self.der*other)
    def __pow__(self, other):
        if isinstance(other, self.__class__):
            new_val = self.val ** other.val
            new_der = new_val * (other.der * math.log(self.val) + other.val * self.der/self.val)
            return Var(new_val, new_der)
        else:
            new_val = self.val ** other
            new_der = self.der * other * (self.val ** (other - 1))
            return Var(new_val, new_der)
    def __rpow__(self,other):
        if isinstance(other, self.__class__):
            new_val = other.val ** self.val
            new_der = new_val * (self.der * math.log(other.val) + self.val * other.der/other.val)
            return Var(new_val, new_der)
        else:
            new_val = other ** self.val
            new_der = new_val * math.log(other) * self.der
            return Var(new_val, new_der)
    def __neg__(self):
        return Var(-self.val, -self.der)
    def __sub__(self,other):
        if isinstance(other, self.__class__):
            return Var(self.val - other.val, self.der - other.der)
        else:
            return Var(self.val - other, self.der)
    def __rsub__(self,other):
        if isinstance(other, self.__class__):
            return Var(other.val - self.val, other.der - self.der)
        else:
            return Var(other - self.val, -self.der)
    def __truediv__(self,other):
        if isinstance(other, self.__class__):
            new_val = self.val/other.val
            new_der = (self.der*other.val - self.val*other.der)/(other.val**2)
            return Var(new_val, new_der)
        else:
            return Var(self.val/other, self.der/other)
    def __rtruediv__(self,other):
        if isinstance(other, self.__class__):
            new_val = other.val/self.val
            new_der = (other.der*self.val - other.val*self.der)/(self.val**2)
            return Var(new_val, new_der)
        else:
            return Var(other/self.val, -other*self.der/(self.val ** 2))
        
        
    __radd__ = __add__
    __rmul__ = __mul__
        
def sin(var):
    if isinstance(var, tuple):
        deriv = 0
        val = 1
        for i in range(len(var)):
            deriv_part = var[i].der
            inner_value = var[i].val
            for j in range(len(var)):
                if i != j:
                    deriv_part *= var[j].val
                    inner_value *= var[j].val
            deriv += deriv_part * math.cos(inner_value)
            val *= math.sin(var[j].val)
        return Var(val, deriv)
    if isinstance(var,Var(0,0).__class__):
        return Var(math.sin(var.val), var.der * math.cos(var.val))
    else:
        return math.sin(var)

def cos(var):
    if isinstance(var, tuple):
        deriv = 0
        val = 1
        for i in range(len(var)):
            deriv_part = var[i].der
            inner_value = var[i].val
            for j in range(len(var)):
                if i != j:
                    deriv_part *= var[j].val
                    inner_value *= var[j].val
            deriv -= deriv_part * math.sin(inner_value)
            val *= math.cos(var[j].val)
        return Var(val, -deriv)
    if isinstance(var,Var(0,0).__class__):
        return Var(math.cos(var.val), -var.der * math.sin(var.val))
    else:
        return math.cos(var)

def funct(x,y):
    #f1 = (y+neg(x**2))**2 + (1+ neg(x))**2
    #f1 = sum((pow(2,y), c(2,neg(product((y, pow(2,x))))), pow(4,x), neg(c(2,x)), pow(2,x)))
    #f1 = sum([y**2 - 2*(y * x**2) + x**4 -(2*x) + x**2])
    #f1 = y**2 - 2*(y * x**2) + x**4 -(2*x) + x**2
    f1 = (y-x**2)**2 + (1-x)**2
    return f1 

def compute_grad(vars):
    grad = [0] * len(vars) 
    for i in range(len(vars)):
        vars[i].der = 1
        grad[i] = funct(*vars).der
        vars[i].der = 0
    return grad

def funct_a4(x, y):
    return (y-(5.1*x**2)/(4*pi**2) + (5*x)/pi-6)**2 + 10*(1-1/(8*pi))*cos(x) + 10 

def compute_grad_a4(vars):
    grad = [0] * len(vars) 
    for i in range(len(vars)):
        vars[i].der = 1
        grad[i] = funct_a4(*vars).der
        vars[i].der = 0
    return grad    

def main():
     x = Var(3, 1)
     y = Var(5, 0)
     z = Var(2, 0)
     
     u = x+y
     print(u)
     
     f = funct(x,y)
     print(f.der)
    
     x.der = 0
     y.der = 1
     f = funct(x,y)
     print(f.der)
    
     x = Var(3, 1)
     y = Var(5, 0)
     z = Var(2, 0)
     vars = (x, y)
     grad = compute_grad(vars)
     print(grad)


#main()

