/*jslint browser: true*/
/*global console*/

var myapp = myapp || {};
myapp.pages = myapp.pages || {};

myapp.pages.IndexPageController = function (myapp, $$) {
  'use strict';
  
  // Init method
  (function () {
    var options = {
      'bgcolor': '#0da6ec',
      'fontcolor': '#fff',
      'onOpened': function () {
        console.log("welcome screen opened");
      },
      'onClosed': function () {
        console.log("welcome screen closed");
      }
    },
    welcomescreen_slides = [
      {
        id: 'slide0',
        picture: '<div class="tutorialicon">♥</div>',
        text: '关心你的电力<a class="tutorial-next-link" href="#" style="text-decoration: none;">-下一页</a>'
      },
      {
        id: 'slide1',
        picture: '<div class="tutorialicon">✲</div>',
        text: '关心电力安全<a class="tutorial-next-link" href="#" style="text-decoration: none;">-下一页</a>'
      },
      {
        id: 'slide2',
        picture: '<div class="tutorialicon">☆</div>',
        text: '全心为你' +
        '<br><br><a class="tutorial-close-btn" href="#">马上进入</a>'
      }
    ],
    welcomescreen = myapp.welcomescreen(welcomescreen_slides, options);
    
    $$(document).on('click', '.tutorial-close-btn', function () {
      welcomescreen.close();
    });

    $$('.tutorial-open-btn').click(function () {
      welcomescreen.open();  
    });
    
    $$(document).on('click', '.tutorial-next-link', function (e) {
      welcomescreen.next(); 
    });
    
    $$(document).on('click', '.tutorial-previous-slide', function (e) {
      welcomescreen.previous(); 
    });
  
  }());

};