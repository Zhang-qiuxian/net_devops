import pickle
import base64

b: str = 'gASVOAAAAAAAAAB9lCiMB3N1Y2Nlc3OUiIwHbWVzc2FnZZSMG+aJgOacieiuvuWkh+mDveW3suWQjOatpe+8gZR1Lg=='
r = base64.b64decode(b)
print(r)
print(pickle.loads(r))

m: str = '所有设备都已同步！'
print(pickle.dumps(m))
