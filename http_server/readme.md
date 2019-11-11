## 设置模块灯光闪烁频率的api


##### url: http://{host}/u?action=setbinkfreq
>url exmaple: `192.168.0.76/u?apikey=f6fdffe48c908deb0f4c3bd36c032e72&action=set_blinkfreq`

#####  方法:post

#####  数据body:json格式。{"data":[{}]}

要求的输入格式与腾讯的风格保持一致，sample如下：

```
{
    "data": [
        {
        "u_id": "PMS811A9A9CDCDB6",
        "u_blinkfreq":3000
    }
  ]
}
```

- u_id指要修改的模块id。
- u_blinkfreq 模块闪烁的周期，单位毫秒，范围500-3000的整数。
- 可以同时修改多个模块的闪烁频率。
