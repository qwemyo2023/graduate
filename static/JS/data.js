let DATA = {
    // todolist 목록 
  };
  
Date.prototype.format = function () {  // 현재 날짜 보기좋게 출력 / 사용방법: newDate().format() 으로 사용가능
    var yyyy = this.getFullYear();
    var month = (this.getMonth() + 1);
    var dd = this.getDate();
    var format = [yyyy, month, dd].join('-');
    return format;
  }
  
Date.prototype.format2 = function () {  // 현재 날짜 보기좋게 출력 / 사용방법: newDate().format() 으로 사용가능
    var yyyy = this.getFullYear();
    var month = (this.getMonth() + 1);
    var format = [yyyy, month].join('-');
    return format;
  }

Date.prototype.format = function(f) {
    if (!this.valueOf()) return " ";

    var weekName = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];
    var d = this;

    return f.replace(/(yyyy|yy|MM|dd|E|hh|mm|ss|a\/p)/gi, function($1) {
        switch ($1) {
            case "yyyy": return d.getFullYear();
            case "yy": return (d.getFullYear() % 1000).zf(2);
            case "MM": return (d.getMonth() + 1).zf(2);
            case "dd": return d.getDate().zf(2);
            case "E": return weekName[d.getDay()];
            case "HH": return d.getHours().zf(2);
            case "hh": return ((h = d.getHours() % 12) ? h : 12).zf(2);
            case "mm": return d.getMinutes().zf(2);
            case "ss": return d.getSeconds().zf(2);
            case "a/p": return d.getHours() < 12 ? "오전" : "오후";
            default: return $1;
        }
    });
};

String.prototype.string = function(len){var s = '', i = 0; while (i++ < len) { s += this; } return s;};
String.prototype.zf = function(len){return "0".string(len - this.length) + this;};
Number.prototype.zf = function(len){return this.toString().zf(len);};

document.write(new Date().format("yyyy/MM/dd</br>"));
document.write(new Date().format("HH:mm:ss</br>"));