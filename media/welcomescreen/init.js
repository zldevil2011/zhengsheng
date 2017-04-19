/*jslint browser: true*/
/*global console, Framework7, angular, Dom7*/

var myapp = myapp || {};

myapp.init = (function () {
  'use strict';
  
  var exports = {};
  
  document.addEventListener("DOMContentLoaded", function(event) {
      // 判断是否是一次打开
      try{
          var storage = window.localStorage;
          var first = storage.getItem("zhengsheng_welcome");
          console.log(first);
          if(first == 1){
              // 不是第一次打开
          }else{
              var fw7App = new Framework7(),
              fw7ViewOptions = {
                  dynamicNavbar: true,
                  domCache: true
              },
              mainView = fw7App.addView('.view-main', fw7ViewOptions),
              $$ = Dom7,
              ipc = new myapp.pages.IndexPageController(fw7App, $$);
              storage.setItem("zhengsheng_welcome", 1);
          }
      }
      catch (e){
          var fw7App = new Framework7(),
              fw7ViewOptions = {
                  dynamicNavbar: true,
                  domCache: true
              },
              mainView = fw7App.addView('.view-main', fw7ViewOptions),
              $$ = Dom7,
              ipc = new myapp.pages.IndexPageController(fw7App, $$);
      }
      // Initialize app

  });
  
  return exports;

}());