玉符单点登录 SDK
======
玉符SDK集成了签署和验证JWT令牌的功能，使得身份提供者（IDP）和服务提供者（SP）只需要用很少的工作量就可以快速将玉符提供的单点登录等功能集成到现有的服务中。

## 单点登录SDK简介

* 作为服务提供者（SP）,可以使用玉符SDK验证JWT令牌的有效性（包括有效期、签名等），验证成功后可取出token中字段进行相应的鉴权。
* 作为身份提供者（IDP）,可以使用玉符SDK灵活进行参数配置，并生成带有token的跳转url，进行单点登录功能。

## 使用SDK
**服务提供者(SP)**
1. 使用必要信息初始化SDK
```
 //方法1:使用公钥路径初始化
 serviceProvider = YufuAuth.builder()
             .role("SP")
             .publicKeyPath({keyPath})
             .build();
             
```

2. 实现单点登录：接收并验证`verify`JWT令牌的有效性（包括有效期、签名等），如通过，说明该令牌来自玉符信任的有效租户(企业/组织)的用户，样例
```
  claims = serviceProvider.verify(idToken);       // 使用验证玉符SDK实例进行验证, 如果成功会返回包含用户信息的对象，失败则会产生授权错误的异常
```

3. 根据第2步获取的用户信息，服务提供商(SP)在token验证通过后，取出token中subject等必要信息，进行相应登录鉴权，否则提示用户登录失败

 