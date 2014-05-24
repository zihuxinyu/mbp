/**
 * Created by weibaohui on 14-5-24.
 */


function GetParams(url, c) {
    if (!url) url = location.href;
    if (!c) c = "?";
    url = url.split(c)[1];
    var params = {};
if (url) {
    var us = url.split("&");
    for (var i = 0, l = us.length; i < l; i++) {
    var ps = us[i].split("=");
    params[ps[0]] = decodeURIComponent(ps[1]);
    }
}
return params;
}



function onSkinChange(skin) {
    //mini.Cookie.set('miniuiSkin', skin);
    mini.Cookie.set('miniuiSkin', skin, 100);//100天过期的话，可以保持皮肤切换
    window.location.reload()
    }
function AddCSSLink(id, url, doc) {
    doc = doc || document;
    var link = doc.createElement("link");
    link.id = id;
    link.setAttribute("rel", "stylesheet");
    link.setAttribute("type", "text/css");
    link.setAttribute("href", url);

    var heads = doc.getElementsByTagName("head");
    if (heads.length)
    heads[0].appendChild(link);
    else
    doc.documentElement.appendChild(link);
    }



