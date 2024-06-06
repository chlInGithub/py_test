
const Crypto = require("./crypto-js");


// var r = 36e5; // 3600秒
// 加密方法
const encrypt = function (e, t, n) {
    var r = Crypto.enc.Utf8.parse(n),
        a = Crypto.enc.Utf8.parse(e),
        i = Crypto.enc.Utf8.parse(t),
        u = Crypto.AES.encrypt(r, a, {
            iv: i,
            mode: Crypto.mode.CBC,
            padding: Crypto.pad.Pkcs7
        });
    return u.ciphertext.toString(Crypto.enc.Hex)
};

// 加密
const handleEncrypt = function (t, n, e) {
    //var t = "5bdb8d6983fe5b459f7d1a843f202273", // token
    //    n = "1709190725621"; // 登陆时间
    var r = Crypto.SHA1(n + "");
    var i = encrypt(t, r.toString().substring(0, 16), e);
    return  i.substring(0, 7) + "0" + i.substring(7)
};

// 获取命令行参数
const args = process.argv.slice(2); // process.argv[0] 是 node，process.argv[1] 是脚本文件路径
console.log(handleEncrypt(args[0], args[1], args[2])) // 0 token，1 time，2 openId

//console.log(handleEncrypt("oiJ7_w5yZav4Vb8GRgof-WdcybHU"))
//console.log(handledDecrypt("ucNKhKrPWiwz0FygrZB670ofKxjlZmZS9poqjn1/axUcNqjlw+BuXQHZe4gjz+EmViGFPE+k7E/+S13GJh1QqDx2awWDe18iQTbMlRHsRj+vn2Guq6CoePY2bhJHRYNq4byVJuxuBpnEgF58Yx7qjm4EJ36cTubtYDPu9nR/rKcjRJJpQGwrDzezzDIhYEfWM81KVCV+voSVMlVAo/iunuAe+c15Rpv/8Kd4XKwT0cTtQybIkwLvh/ihDOuq5O9Zpr3DNwKgjLPpB0Cj8KX7tb7oUhL9/w4TtJ4u7qv882OxBXSfQsFo711nb+vkU6vyHUqa/A/dB93fVX3Xi3AX0zU07+d1rBuahFyxq0+5eJVhpV0BjTs2XCRcT/xUUiN2"))
