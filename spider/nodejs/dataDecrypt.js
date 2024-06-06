
const Crypto = require("./crypto-js");
const fs = require('fs').promises;


async function readFileContent(file) {
    try {
        const data = await fs.readFile(file, 'utf8');
        return data; // The spell is complete, and the data is returned
    } catch (err) {
        throw err; // Alas, if an error occurs, it is thrown to be dealt with by higher powers
    }
}

// 解密方法
const decrypt = async function (e, t, n) {

    const data = await readFileContent(n);
    //console.log("begin");
    //console.log(data);
    //console.log("end");
    var r = Crypto.enc.Base64.parse(data),
        a = Crypto.enc.Utf8.parse(e),
        i = Crypto.enc.Utf8.parse(t),
        u = Crypto.AES.decrypt({
            ciphertext: r
        }, a, {
            iv: i,
            mode: Crypto.mode.CBC,
            padding: Crypto.pad.Pkcs7
        });
    return (u.toString(Crypto.enc.Utf8))

};
// 解密
const handledDecrypt = async function (t, n, dataStr) {
    //var t = "5bdb8d6983fe5b459f7d1a843f202273", // token
    //    n = "1709190725621", // 登陆时间
    var r = Crypto.SHA1(n + "");
    return await decrypt(t, r.toString().substring(0, 16), dataStr)
    //return JSON.parse(decrypt(t, r.toString().substring(0, 16), dataStr))
};

// 获取命令行参数
const args = process.argv.slice(2); // process.argv[0] 是 node，process.argv[1] 是脚本文件路径
handledDecrypt(args[0],args[1],args[2]).then(result => console.log(result))
//console.log(data) // 0 token, 1 time, 2 data

//console.log(handleEncrypt("oiJ7_w5yZav4Vb8GRgof-WdcybHU"))
//console.log(handledDecrypt("ucNKhKrPWiwz0FygrZB670ofKxjlZmZS9poqjn1/axUcNqjlw+BuXQHZe4gjz+EmViGFPE+k7E/+S13GJh1QqDx2awWDe18iQTbMlRHsRj+vn2Guq6CoePY2bhJHRYNq4byVJuxuBpnEgF58Yx7qjm4EJ36cTubtYDPu9nR/rKcjRJJpQGwrDzezzDIhYEfWM81KVCV+voSVMlVAo/iunuAe+c15Rpv/8Kd4XKwT0cTtQybIkwLvh/ihDOuq5O9Zpr3DNwKgjLPpB0Cj8KX7tb7oUhL9/w4TtJ4u7qv882OxBXSfQsFo711nb+vkU6vyHUqa/A/dB93fVX3Xi3AX0zU07+d1rBuahFyxq0+5eJVhpV0BjTs2XCRcT/xUUiN2"))
