class KRIPTO_lib():

    def fast_pow_mod(self, x, pow, mod):
        res = 1
        pow_res = 0
        while pow_res < pow:
            pow_res_1 = 2
            res1 = x
            while pow_res + pow_res_1 <= pow:
                res1 = (res1 * res1) % mod
                pow_res_1 *= 2
            pow_res_1 //= 2
            res = (res * res1) % mod
            pow_res += pow_res_1
        return res % mod
    
    def my_gcd(self, x, y):
        while x != 0 and y != 0:
            if x >= y:
                x %= y
            else:
                y %= x
        return x or y
    
    def hall(self,p,g,xa,xb):
        ya = self.fast_pow_mod(x=g, pow=xa, mod=p)
        yb = self.fast_pow_mod(x=g, pow=xb, mod=p)
        Zab = self.fast_pow_mod(x=ya, pow=xb, mod=p)
        Zba = self.fast_pow_mod(x=yb, pow=xa, mod=p)
        return ya, yb, Zab, Zba

    def evkl(self, a, b):
        if a>b:
            u = [a, 1, 0]
            v = [b, 0, 1]
        else:
            u = [b, 1, 0]
            v = [a, 0, 1]
        q = a//b
        t = [u[0]%v[0],u[1]-q*v[1],u[2]-q*v[2]]
        while t[0] != 1:
            u = v
            v = t
            v[0] = t[0]
            q = u[0]//v[0]
            if t[0] == 0 or t[0] == 1:
                break
            t = [u[0]%v[0],u[1]-q*v[1],u[2]-q*v[2]]
        return t
                
            
    
test = KRIPTO_lib()
print(test.evkl(28,19))
