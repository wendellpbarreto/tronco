// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

/* jQuery FlexSlider v1.8
 * http://flex.madebymufffin.com
 *
 * Copyright 2011, Tyler Smith
 * Free to use under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Contrib: Darin Richardson
 */

  ;(function ($) {
    
    //FlexSlider: Object Instance
    $.flexslider = function(el, options) {
      var slider = el;

      slider.init = function() {
        slider.vars = $.extend({}, $.flexslider.defaults, options);
        slider.data('flexslider', true);
        slider.container = $('.slides', slider);
        slider.slides = $('.slides > li', slider);
        slider.count = slider.slides.length;
        slider.animating = false;
        slider.currentSlide = slider.vars.slideToStart;
        slider.animatingTo = slider.currentSlide;
        slider.atEnd = (slider.currentSlide == 0) ? true : false;
        slider.eventType = ('ontouchstart' in document.documentElement) ? 'touchstart' : 'click';
        slider.cloneCount = 0;
        slider.cloneOffset = 0;
        slider.manualPause = false;
        slider.vertical = (slider.vars.slideDirection == "vertical");
        slider.prop = (slider.vertical) ? "top" : "marginLeft";
        slider.args = {};
        
        //Test for webbkit CSS3 Animations
        slider.transitions = "webkitTransition" in document.body.style;
        if (slider.transitions) slider.prop = "-webkit-transform";
        
        //Test for controlsContainer
        if (slider.vars.controlsContainer != "") {
          slider.controlsContainer = $(slider.vars.controlsContainer).eq($('.slides').index(slider.container));
          slider.containerExists = slider.controlsContainer.length > 0;
        }

        //Test for manualControls
        if (slider.vars.manualControls != "") {
          slider.manualControls = $(slider.vars.manualControls, ((slider.containerExists) ? slider.controlsContainer : slider));
          slider.manualExists = slider.manualControls.length > 0;
        }
        
        ///////////////////////////////////////////////////////////////////
        // FlexSlider: Randomize Slides
        if (slider.vars.randomize) {
          slider.slides.sort(function() { return (Math.round(Math.random())-0.5); });
          slider.container.empty().append(slider.slides);
        }
        ///////////////////////////////////////////////////////////////////
        
        ///////////////////////////////////////////////////////////////////
        // FlexSlider: Slider Animation Initialize
        if (slider.vars.animation.toLowerCase() == "slide") {
          if (slider.transitions) {
            slider.setTransition(0);
          }
          slider.css({"overflow": "hidden"});
          if (slider.vars.animationLoop) {
            slider.cloneCount = 2;
            slider.cloneOffset = 1;
            slider.container.append(slider.slides.filter(':first').clone().addClass('clone')).prepend(slider.slides.filter(':last').clone().addClass('clone'));
          }
          //create newSlides to capture possible clones
          slider.newSlides = $('.slides > li', slider);
          var sliderOffset = (-1 * (slider.currentSlide + slider.cloneOffset));
          if (slider.vertical) {
            slider.newSlides.css({"display": "block", "width": "100%", "float": "left"});
            slider.container.height((slider.count + slider.cloneCount) * 200 + "%").css("position", "absolute").width("100%");
            //Timeout function to give browser enough time to get proper height initially
            setTimeout(function() {
              slider.css({"position": "relative"}).height(slider.slides.filter(':first').height());
              slider.args[slider.prop] = (slider.transitions) ? "translate3d(0," + sliderOffset * slider.height() + "px,0)" : sliderOffset * slider.height() + "px";
              slider.container.css(slider.args);
            }, 100);

          } else {
            slider.args[slider.prop] = (slider.transitions) ? "translate3d(" + sliderOffset * slider.width() + "px,0,0)" : sliderOffset * slider.width() + "px";
            slider.container.width((slider.count + slider.cloneCount) * 200 + "%").css(slider.args);
            //Timeout function to give browser enough time to get proper width initially
            setTimeout(function() {
              slider.newSlides.width(slider.width()).css({"float": "left", "display": "block"});
            }, 100);
          }
          
        } else { //Default to fade
          //Not supporting fade CSS3 transitions right now
          slider.transitions = false;
          slider.slides.css({"width": "100%", "float": "left", "marginRight": "-100%"}).eq(slider.currentSlide).fadeIn(slider.vars.animationDuration); 
        }
        ///////////////////////////////////////////////////////////////////
        
        ///////////////////////////////////////////////////////////////////
        // FlexSlider: Control Nav
        if (slider.vars.controlNav) {
          if (slider.manualExists) {
            slider.controlNav = slider.manualControls;
          } else {
            var controlNavScaffold = $('<ol class="flex-control-nav"></ol>');
            var j = 1;
            for (var i = 0; i < slider.count; i++) {
              controlNavScaffold.append('<li><a>' + j + '</a></li>');
              j++;
            }

            if (slider.containerExists) {
              $(slider.controlsContainer).append(controlNavScaffold);
              slider.controlNav = $('.flex-control-nav li a', slider.controlsContainer);
            } else {
              slider.append(controlNavScaffold);
              slider.controlNav = $('.flex-control-nav li a', slider);
            }
          }

          slider.controlNav.eq(slider.currentSlide).addClass('active');

          slider.controlNav.bind(slider.eventType, function(event) {
            event.preventDefault();
            if (!$(this).hasClass('active')) {
              (slider.controlNav.index($(this)) > slider.currentSlide) ? slider.direction = "next" : slider.direction = "prev";
              slider.flexAnimate(slider.controlNav.index($(this)), slider.vars.pauseOnAction);
            }
          });
        }
        ///////////////////////////////////////////////////////////////////
        
        //////////////////////////////////////////////////////////////////
        //FlexSlider: Direction Nav
        if (slider.vars.directionNav) {
          slider.directionNav = $('.flex-direction-nav a', slider);        
          
          //Set initial disable styles if necessary
          // if (!slider.vars.animationLoop) {
          //   if (slider.currentSlide == 0) {
          //     slider.directionNav.filter('.prev').addClass('disabled');
          //   } else if (slider.currentSlide == slider.count - 1) {
          //     slider.directionNav.filter('.next').addClass('disabled');
          //   }
          // }
          
          slider.directionNav.bind(slider.eventType, function(event) {
            event.preventDefault();
            var target = ($(this).hasClass('next')) ? slider.getTarget('next') : slider.getTarget('prev');
            if (!$(this).hasClass('disabled')){
              if (slider.canAdvance(target)) {
                slider.flexAnimate(target, slider.vars.pauseOnAction);
              }
            }
          });
        }
        //////////////////////////////////////////////////////////////////
        
        //////////////////////////////////////////////////////////////////
        //FlexSlider: Keyboard Nav
        if (slider.vars.keyboardNav && $('ul.slides').length == 1) {
          function keyboardMove(event) {
            if (slider.animating) {
              return;
            } else if (event.keyCode != 39 && event.keyCode != 37){
              return;
            } else {
              if (event.keyCode == 39) {
                var target = slider.getTarget('next');
              } else if (event.keyCode == 37){
                var target = slider.getTarget('prev');
              }
          
              if (slider.canAdvance(target)) {
                slider.flexAnimate(target, slider.vars.pauseOnAction);
              }
            }
          }
          $(document).bind('keyup', keyboardMove);
        }
        //////////////////////////////////////////////////////////////////
        
        ///////////////////////////////////////////////////////////////////
        // FlexSlider: Mousewheel interaction
        if (slider.vars.mousewheel) {
          slider.mousewheelEvent = (/Firefox/i.test(navigator.userAgent)) ? "DOMMouseScroll" : "mousewheel";
          slider.bind(slider.mousewheelEvent, function(e) {
            e.preventDefault();
            e = e ? e : window.event;
            var wheelData = e.detail ? e.detail * -1 : e.wheelDelta / 40,
                target = (wheelData < 0) ? slider.getTarget('next') : slider.getTarget('prev');
            
            if (slider.canAdvance(target)) {
              slider.flexAnimate(target, slider.vars.pauseOnAction);
            }
          });
        }
        ///////////////////////////////////////////////////////////////////
        
        //////////////////////////////////////////////////////////////////
        //FlexSlider: Slideshow Setup
        if (slider.vars.slideshow) {
          //pauseOnHover
          if (slider.vars.pauseOnHover && slider.vars.slideshow) {
            slider.hover(function() {
              slider.pause();
            }, function() {
              if (!slider.manualPause) {
                slider.resume();
              }
            });
          }

          //Initialize animation
          slider.animatedSlides = setInterval(slider.animateSlides, slider.vars.slideshowSpeed);
        }
        //////////////////////////////////////////////////////////////////
        
        //////////////////////////////////////////////////////////////////
        //FlexSlider: Pause/Play
        if (slider.vars.pausePlay) {
          var pausePlayScaffold = $('<div class="flex-pauseplay"><span></span></div>');
        
          if (slider.containerExists) {
            slider.controlsContainer.append(pausePlayScaffold);
            slider.pausePlay = $('.flex-pauseplay span', slider.controlsContainer);
          } else {
            slider.append(pausePlayScaffold);
            slider.pausePlay = $('.flex-pauseplay span', slider);
          }
          
          var pausePlayState = (slider.vars.slideshow) ? 'pause' : 'play';
          slider.pausePlay.addClass(pausePlayState).text((pausePlayState == 'pause') ? slider.vars.pauseText : slider.vars.playText);
          
          slider.pausePlay.bind(slider.eventType, function(event) {
            event.preventDefault();
            if ($(this).hasClass('pause')) {
              slider.pause();
              slider.manualPause = true;
            } else {
              slider.resume();
              slider.manualPause = false;
            }
          });
        }
        //////////////////////////////////////////////////////////////////
        
        //////////////////////////////////////////////////////////////////
        //FlexSlider:Touch Swip Gestures
        //Some brilliant concepts adapted from the following sources
        //Source: TouchSwipe - http://www.netcu.de/jquery-touchwipe-iphone-ipad-library
        //Source: SwipeJS - http://swipejs.com
        if ('ontouchstart' in document.documentElement) {
          //For brevity, variables are named for x-axis scrolling
          //The variables are then swapped if vertical sliding is applied
          //This reduces redundant code...I think :)
          //If debugging, recognize variables are named for horizontal scrolling
          var startX,
            startY,
            offset,
            cwidth,
            dx,
            startT,
            scrolling = false;
                
          slider.each(function() {
            if ('ontouchstart' in document.documentElement) {
              this.addEventListener('touchstart', onTouchStart, false);
            }
          });
          
          function onTouchStart(e) {
            if (slider.animating) {
              e.preventDefault();
            } else if (e.touches.length == 1) {
              slider.pause();
              cwidth = (slider.vertical) ? slider.height() : slider.width();
              startT = Number(new Date());
              offset = (slider.vertical) ? (slider.currentSlide + slider.cloneOffset) * slider.height() : (slider.currentSlide + slider.cloneOffset) * slider.width();
              startX = (slider.vertical) ? e.touches[0].pageY : e.touches[0].pageX;
              startY = (slider.vertical) ? e.touches[0].pageX : e.touches[0].pageY;
              slider.setTransition(0);

              this.addEventListener('touchmove', onTouchMove, false);
              this.addEventListener('touchend', onTouchEnd, false);
            }
          }

          function onTouchMove(e) {
            dx = (slider.vertical) ? startX - e.touches[0].pageY : startX - e.touches[0].pageX;
            scrolling = (slider.vertical) ? (Math.abs(dx) < Math.abs(e.touches[0].pageX - startY)) : (Math.abs(dx) < Math.abs(e.touches[0].pageY - startY));

            if (!scrolling) {
              e.preventDefault();
              if (slider.vars.animation == "slide" && slider.transitions) {
                if (!slider.vars.animationLoop) {
                  dx = dx/((slider.currentSlide == 0 && dx < 0 || slider.currentSlide == slider.count - 1 && dx > 0) ? (Math.abs(dx)/cwidth+2) : 1);
                }
                slider.args[slider.prop] = (slider.vertical) ? "translate3d(0," + (-offset - dx) + "px,0)": "translate3d(" + (-offset - dx) + "px,0,0)";
                slider.container.css(slider.args);
              }
            }
          }
          
          function onTouchEnd(e) {
            slider.animating = false;
            if (slider.animatingTo == slider.currentSlide && !scrolling && !(dx == null)) {
              var target = (dx > 0) ? slider.getTarget('next') : slider.getTarget('prev');
              if (slider.canAdvance(target) && Number(new Date()) - startT < 550 && Math.abs(dx) > 20 || Math.abs(dx) > cwidth/2) {
                slider.flexAnimate(target, slider.vars.pauseOnAction);
              } else {
                slider.flexAnimate(slider.currentSlide, slider.vars.pauseOnAction);
              }
            }
            
            //Finish the touch by undoing the touch session
            this.removeEventListener('touchmove', onTouchMove, false);
            this.removeEventListener('touchend', onTouchEnd, false);
            startX = null;
            startY = null;
            dx = null;
            offset = null;
          }
        }
        //////////////////////////////////////////////////////////////////
        
        //////////////////////////////////////////////////////////////////
        //FlexSlider: Resize Functions (If necessary)
        if (slider.vars.animation.toLowerCase() == "slide") {
          $(window).resize(function(){
            if (!slider.animating) {
              if (slider.vertical) {
                slider.height(slider.slides.filter(':first').height());
                slider.args[slider.prop] = (-1 * (slider.currentSlide + slider.cloneOffset))* slider.slides.filter(':first').height() + "px";
                if (slider.transitions) {
                  slider.setTransition(0);
                  slider.args[slider.prop] = (slider.vertical) ? "translate3d(0," + slider.args[slider.prop] + ",0)" : "translate3d(" + slider.args[slider.prop] + ",0,0)";
                }
                slider.container.css(slider.args);
              } else {
                slider.newSlides.width(slider.width());
                slider.args[slider.prop] = (-1 * (slider.currentSlide + slider.cloneOffset))* slider.width() + "px";
                if (slider.transitions) {
                  slider.setTransition(0);
                  slider.args[slider.prop] = (slider.vertical) ? "translate3d(0," + slider.args[slider.prop] + ",0)" : "translate3d(" + slider.args[slider.prop] + ",0,0)";
                }
                slider.container.css(slider.args);
              }
            }
          });
        }
        //////////////////////////////////////////////////////////////////
        
        //////////////////////////////////////////////////////////////////
        //FlexSlider: Destroy the slider entity
        //Destory is not included in the minified version right now, but this is a working function for anyone who wants to include it.
        //Simply bind the actions you need from this function into a function in the start() callback to the event of your chosing
        /*
        slider.destroy = function() {
          slider.pause();
          if (slider.controlNav && slider.vars.manualControls == "") slider.controlNav.closest('.flex-control-nav').remove();
          if (slider.directionNav) slider.directionNav.closest('.flex-direction-nav').remove();
          if (slider.vars.pausePlay) slider.pausePlay.closest('.flex-pauseplay').remove();
          if (slider.vars.keyboardNav && $('ul.slides').length == 1) $(document).unbind('keyup', keyboardMove);
          if (slider.vars.mousewheel) slider.unbind(slider.mousewheelEvent);
          if (slider.transitions) slider.each(function(){this.removeEventListener('touchstart', onTouchStart, false);});
          if (slider.vars.animation == "slide" && slider.vars.animationLoop) slider.newSlides.filter('.clone').remove();
          if (slider.vertical) slider.height("auto");
          slider.slides.hide();
          slider.removeData('flexslider');
        }
        */
        //////////////////////////////////////////////////////////////////
        
        //FlexSlider: start() Callback
        slider.vars.start(slider);
      }
      
      //FlexSlider: Animation Actions
      slider.flexAnimate = function(target, pause) {
        if (!slider.animating) {
          //Animating flag
          slider.animating = true;
          
          //FlexSlider: before() animation Callback
          slider.animatingTo = target;
          slider.vars.before(slider);
          
          //Optional paramter to pause slider when making an anmiation call
          if (pause) {
            slider.pause();
          }
          
          //Update controlNav   
          if (slider.vars.controlNav) {
            slider.controlNav.removeClass('active').eq(target).addClass('active');
          }
          
          //Is the slider at either end
          slider.atEnd = (target == 0 || target == slider.count - 1) ? true : false;
          if (!slider.vars.animationLoop && slider.vars.directionNav) {
            // if (target == 0) {
            //   slider.directionNav.removeClass('disabled').filter('.prev').addClass('disabled');
            // } else if (target == slider.count - 1) {
            //   slider.directionNav.removeClass('disabled').filter('.next').addClass('disabled');
            // } else {
            //   slider.directionNav.removeClass('disabled');
            // }
          }
          
          if (!slider.vars.animationLoop && target == slider.count - 1) {
            slider.pause();
            //FlexSlider: end() of cycle Callback
            slider.vars.end(slider);
          }
          
          if (slider.vars.animation.toLowerCase() == "slide") {
            var dimension = (slider.vertical) ? slider.slides.filter(':first').height() : slider.slides.filter(':first').width();
            
            if (slider.currentSlide == 0 && target == slider.count - 1 && slider.vars.animationLoop && slider.direction != "next") {
              slider.slideString = "0px";
            } else if (slider.currentSlide == slider.count - 1 && target == 0 && slider.vars.animationLoop && slider.direction != "prev") {
              slider.slideString = (-1 * (slider.count + 1)) * dimension + "px";
            } else {
              slider.slideString = (-1 * (target + slider.cloneOffset)) * dimension + "px";
            }
            slider.args[slider.prop] = slider.slideString;

            if (slider.transitions) {
                slider.setTransition(slider.vars.animationDuration); 
                slider.args[slider.prop] = (slider.vertical) ? "translate3d(0," + slider.slideString + ",0)" : "translate3d(" + slider.slideString + ",0,0)";
                slider.container.css(slider.args).one("webkitTransitionEnd transitionend", function(){
                  slider.wrapup(dimension);
                });   
            } else {
              slider.container.animate(slider.args, slider.vars.animationDuration, function(){
                slider.wrapup(dimension);
              });
            }
          } else { //Default to Fade
            slider.slides.eq(slider.currentSlide).fadeOut(slider.vars.animationDuration);
            slider.slides.eq(target).fadeIn(slider.vars.animationDuration, function() {
              slider.wrapup();
            });
          }
        }
      }
      
      //FlexSlider: Function to minify redundant animation actions
      slider.wrapup = function(dimension) {
        if (slider.vars.animation == "slide") {
          //Jump the slider if necessary
          if (slider.currentSlide == 0 && slider.animatingTo == slider.count - 1 && slider.vars.animationLoop) {
            slider.args[slider.prop] = (-1 * slider.count) * dimension + "px";
            if (slider.transitions) {
              slider.setTransition(0);
              slider.args[slider.prop] = (slider.vertical) ? "translate3d(0," + slider.args[slider.prop] + ",0)" : "translate3d(" + slider.args[slider.prop] + ",0,0)";
            }
            slider.container.css(slider.args);
          } else if (slider.currentSlide == slider.count - 1 && slider.animatingTo == 0 && slider.vars.animationLoop) {
            slider.args[slider.prop] = -1 * dimension + "px";
            if (slider.transitions) {
              slider.setTransition(0);
              slider.args[slider.prop] = (slider.vertical) ? "translate3d(0," + slider.args[slider.prop] + ",0)" : "translate3d(" + slider.args[slider.prop] + ",0,0)";
            }
            slider.container.css(slider.args);
          }
        }
        slider.animating = false;
        slider.currentSlide = slider.animatingTo;
        //FlexSlider: after() animation Callback
        slider.vars.after(slider);
      }
      
      //FlexSlider: Automatic Slideshow
      slider.animateSlides = function() {
        if (!slider.animating) {
          slider.flexAnimate(slider.getTarget("next"));
        }
      }
      
      //FlexSlider: Automatic Slideshow Pause
      slider.pause = function() {
        clearInterval(slider.animatedSlides);
        if (slider.vars.pausePlay) {
          slider.pausePlay.removeClass('pause').addClass('play').text(slider.vars.playText);
        }
      }
      
      //FlexSlider: Automatic Slideshow Start/Resume
      slider.resume = function() {
        slider.animatedSlides = setInterval(slider.animateSlides, slider.vars.slideshowSpeed);
        if (slider.vars.pausePlay) {
          slider.pausePlay.removeClass('play').addClass('pause').text(slider.vars.pauseText);
        }
      }
      
      //FlexSlider: Helper function for non-looping sliders
      slider.canAdvance = function(target) {
        if (!slider.vars.animationLoop && slider.atEnd) {
          if (slider.currentSlide == 0 && target == slider.count - 1 && slider.direction != "next") {
            return false;
          } else if (slider.currentSlide == slider.count - 1 && target == 0 && slider.direction == "next") {
            return false;
          } else {
            return true;
          }
        } else {
          return true;
        }  
      }
      
      //FlexSlider: Helper function to determine animation target
      slider.getTarget = function(dir) {
        slider.direction = dir;
        if (dir == "next") {
          return (slider.currentSlide == slider.count - 1) ? 0 : slider.currentSlide + 1;
        } else {
          return (slider.currentSlide == 0) ? slider.count - 1 : slider.currentSlide - 1;
        }
      }
      
      //FlexSlider: Helper function to set CSS3 transitions
      slider.setTransition = function(dur) {
        slider.container.css({'-webkit-transition-duration': (dur/1000) + "s"});
      }

      //FlexSlider: Initialize
      slider.init();
    }
    
    //FlexSlider: Default Settings
    $.flexslider.defaults = {
      animation: "fade",              //String: Select your animation type, "fade" or "slide"
      slideDirection: "horizontal",   //String: Select the sliding direction, "horizontal" or "vertical"
      slideshow: true,                //Boolean: Animate slider automatically
      slideshowSpeed: 7000,           //Integer: Set the speed of the slideshow cycling, in milliseconds
      animationDuration: 600,         //Integer: Set the speed of animations, in milliseconds
      directionNav: true,             //Boolean: Create navigation for previous/next navigation? (true/false)
      controlNav: true,               //Boolean: Create navigation for paging control of each clide? Note: Leave true for manualControls usage
      keyboardNav: true,              //Boolean: Allow slider navigating via keyboard left/right keys
      mousewheel: false,              //Boolean: Allow slider navigating via mousewheel
      prevText: "Previous",           //String: Set the text for the "previous" directionNav item
      nextText: "Next",               //String: Set the text for the "next" directionNav item
      pausePlay: false,               //Boolean: Create pause/play dynamic element
      pauseText: 'Pause',             //String: Set the text for the "pause" pausePlay item
      playText: 'Play',               //String: Set the text for the "play" pausePlay item
      randomize: false,               //Boolean: Randomize slide order
      slideToStart: 0,                //Integer: The slide that the slider should start on. Array notation (0 = first slide)
      animationLoop: true,            //Boolean: Should the animation loop? If false, directionNav will received "disable" classes at either end
      pauseOnAction: true,            //Boolean: Pause the slideshow when interacting with control elements, highly recommended.
      pauseOnHover: false,            //Boolean: Pause the slideshow when hovering over slider, then resume when no longer hovering
      controlsContainer: "",          //Selector: Declare which container the navigation elements should be appended too. Default container is the flexSlider element. Example use would be ".flexslider-container", "#container", etc. If the given element is not found, the default action will be taken.
      manualControls: "",             //Selector: Declare custom control navigation. Example would be ".flex-control-nav li" or "#tabs-nav li img", etc. The number of elements in your controlNav should match the number of slides/tabs.
      start: function(){},            //Callback: function(slider) - Fires when the slider loads the first slide
      before: function(){},           //Callback: function(slider) - Fires asynchronously with each slider animation
      after: function(){},            //Callback: function(slider) - Fires after each slider animation completes
      end: function(){}               //Callback: function(slider) - Fires when the slider reaches the last slide (asynchronous)
    }
    
    //FlexSlider: Plugin Function
    $.fn.flexslider = function(options) {
      return this.each(function() {
        if ($(this).find('.slides li').length == 1) {
          $(this).find('.slides li').fadeIn(400);
        }
        else if ($(this).data('flexslider') != true) {
          new $.flexslider($(this), options);
        }
      });
    }  

  })(jQuery);


/* alertify
 * An unobtrusive customizable JavaScript notification system
 *
 * @author Fabien Doiron <fabien.doiron@gmail.com>
 * @copyright Fabien Doiron 2013
 * @license MIT <http://opensource.org/licenses/mit-license.php>
 * @link http://fabien-d.github.com/alertify.js/
 * @module alertify
 * @version 0.3.11
 */
  (function (global, undefined) {
    "use strict";

    var document = global.document,
        Alertify;

    Alertify = function () {

      var _alertify = {},
          dialogs   = {},
          isopen    = false,
          keys      = { ENTER: 13, ESC: 27, SPACE: 32 },
          queue     = [],
          $, btnCancel, btnOK, btnReset, btnResetBack, btnFocus, elCallee, elCover, elDialog, elLog, form, input, getTransitionEvent;

      /**
       * Markup pieces
       * @type {Object}
       */
      dialogs = {
        buttons : {
          holder : "<nav class=\"alertify-buttons\">{{buttons}}</nav>",
          submit : "<button type=\"submit\" class=\"alertify-button alertify-button-ok\" id=\"alertify-ok\">{{ok}}</button>",
          ok     : "<button class=\"alertify-button alertify-button-ok\" id=\"alertify-ok\">{{ok}}</button>",
          cancel : "<button class=\"alertify-button alertify-button-cancel\" id=\"alertify-cancel\">{{cancel}}</button>"
        },
        input   : "<div class=\"alertify-text-wrapper\"><input type=\"text\" class=\"alertify-text\" id=\"alertify-text\"></div>",
        message : "<p class=\"alertify-message\">{{message}}</p>",
        log     : "<article class=\"alertify-log{{class}}\">{{message}}</article>"
      };

      /**
       * Return the proper transitionend event
       * @return {String}    Transition type string
       */
      getTransitionEvent = function () {
        var t,
            type,
            supported   = false,
            el          = document.createElement("fakeelement"),
            transitions = {
              "WebkitTransition" : "webkitTransitionEnd",
              "MozTransition"    : "transitionend",
              "OTransition"      : "otransitionend",
              "transition"       : "transitionend"
            };

        for (t in transitions) {
          if (el.style[t] !== undefined) {
            type      = transitions[t];
            supported = true;
            break;
          }
        }

        return {
          type      : type,
          supported : supported
        };
      };

      /**
       * Shorthand for document.getElementById()
       *
       * @param  {String} id    A specific element ID
       * @return {Object}       HTML element
       */
      $ = function (id) {
        return document.getElementById(id);
      };

      /**
       * Alertify private object
       * @type {Object}
       */
      _alertify = {

        /**
         * Labels object
         * @type {Object}
         */
        labels : {
          ok     : "Sim",
          cancel : "Cancelar"
        },

        /**
         * Delay number
         * @type {Number}
         */
        delay : 5000,

        /**
         * Whether buttons are reversed (default is secondary/primary)
         * @type {Boolean}
         */
        buttonReverse : false,

        /**
         * Which button should be focused by default
         * @type {String} "ok" (default), "cancel", or "none"
         */
        buttonFocus : "ok",

        /**
         * Set the transition event on load
         * @type {[type]}
         */
        transition : undefined,

        /**
         * Set the proper button click events
         *
         * @param {Function} fn    [Optional] Callback function
         *
         * @return {undefined}
         */
        addListeners : function (fn) {
          var hasOK     = (typeof btnOK !== "undefined"),
              hasCancel = (typeof btnCancel !== "undefined"),
              hasInput  = (typeof input !== "undefined"),
              val       = "",
              self      = this,
              ok, cancel, common, key, reset;

          // ok event handler
          ok = function (event) {
            if (typeof event.preventDefault !== "undefined") event.preventDefault();
            common(event);
            if (typeof input !== "undefined") val = input.value;
            if (typeof fn === "function") {
              if (typeof input !== "undefined") {
                fn(true, val);
              }
              else fn(true);
            }
            return false;
          };

          // cancel event handler
          cancel = function (event) {
            if (typeof event.preventDefault !== "undefined") event.preventDefault();
            common(event);
            if (typeof fn === "function") fn(false);
            return false;
          };

          // common event handler (keyup, ok and cancel)
          common = function (event) {
            self.hide();
            self.unbind(document.body, "keyup", key);
            self.unbind(btnReset, "focus", reset);
            if (hasOK) self.unbind(btnOK, "click", ok);
            if (hasCancel) self.unbind(btnCancel, "click", cancel);
          };

          // keyup handler
          key = function (event) {
            var keyCode = event.keyCode;
            if ((keyCode === keys.SPACE && !hasInput) || (hasInput && keyCode === keys.ENTER)) ok(event);
            if (keyCode === keys.ESC && hasCancel) cancel(event);
          };

          // reset focus to first item in the dialog
          reset = function (event) {
            if (hasInput) input.focus();
            else if (!hasCancel || self.buttonReverse) btnOK.focus();
            else btnCancel.focus();
          };

          // handle reset focus link
          // this ensures that the keyboard focus does not
          // ever leave the dialog box until an action has
          // been taken
          this.bind(btnReset, "focus", reset);
          this.bind(btnResetBack, "focus", reset);
          // handle OK click
          if (hasOK) this.bind(btnOK, "click", ok);
          // handle Cancel click
          if (hasCancel) this.bind(btnCancel, "click", cancel);
          // listen for keys, Cancel => ESC
          this.bind(document.body, "keyup", key);
          if (!this.transition.supported) {
            this.setFocus();
          }
        },

        /**
         * Bind events to elements
         *
         * @param  {Object}   el       HTML Object
         * @param  {Event}    event    Event to attach to element
         * @param  {Function} fn       Callback function
         *
         * @return {undefined}
         */
        bind : function (el, event, fn) {
          if (typeof el.addEventListener === "function") {
            el.addEventListener(event, fn, false);
          } else if (el.attachEvent) {
            el.attachEvent("on" + event, fn);
          }
        },

        /**
         * Use alertify as the global error handler (using window.onerror)
         *
         * @return {boolean} success
         */
        handleErrors : function () {
          if (typeof global.onerror !== "undefined") {
            var self = this;
            global.onerror = function (msg, url, line) {
              self.error("[" + msg + " on line " + line + " of " + url + "]", 0);
            };
            return true;
          } else {
            return false;
          }
        },

        /**
         * Append button HTML strings
         *
         * @param {String} secondary    The secondary button HTML string
         * @param {String} primary      The primary button HTML string
         *
         * @return {String}             The appended button HTML strings
         */
        appendButtons : function (secondary, primary) {
          return this.buttonReverse ? primary + secondary : secondary + primary;
        },

        /**
         * Build the proper message box
         *
         * @param  {Object} item    Current object in the queue
         *
         * @return {String}         An HTML string of the message box
         */
        build : function (item) {
          var html    = "",
              type    = item.type,
              message = item.message,
              css     = item.cssClass || "";

          html += "<div class=\"alertify-dialog\">";
          html += "<a id=\"alertify-resetFocusBack\" class=\"alertify-resetFocus\" href=\"#\">Reset Focus</a>";

          if (_alertify.buttonFocus === "none") html += "<a href=\"#\" id=\"alertify-noneFocus\" class=\"alertify-hidden\"></a>";

          // doens't require an actual form
          if (type === "prompt") html += "<div id=\"alertify-form\">";

          html += "<article class=\"alertify-inner\">";
          html += dialogs.message.replace("{{message}}", message);

          if (type === "prompt") html += dialogs.input;

          html += dialogs.buttons.holder;
          html += "</article>";

          if (type === "prompt") html += "</div>";

          html += "<a id=\"alertify-resetFocus\" class=\"alertify-resetFocus\" href=\"#\">Reset Focus</a>";
          html += "</div>";

          switch (type) {
          case "confirm":
            html = html.replace("{{buttons}}", this.appendButtons(dialogs.buttons.cancel, dialogs.buttons.ok));
            html = html.replace("{{ok}}", this.labels.ok).replace("{{cancel}}", this.labels.cancel);
            break;
          case "prompt":
            html = html.replace("{{buttons}}", this.appendButtons(dialogs.buttons.cancel, dialogs.buttons.submit));
            html = html.replace("{{ok}}", this.labels.ok).replace("{{cancel}}", this.labels.cancel);
            break;
          case "alert":
            html = html.replace("{{buttons}}", dialogs.buttons.ok);
            html = html.replace("{{ok}}", this.labels.ok);
            break;
          default:
            break;
          }

          elDialog.className = "alertify alertify-" + type + " " + css;
          elCover.className  = "alertify-cover";
          return html;
        },

        /**
         * Close the log messages
         *
         * @param  {Object} elem    HTML Element of log message to close
         * @param  {Number} wait    [optional] Time (in ms) to wait before automatically hiding the message, if 0 never hide
         *
         * @return {undefined}
         */
        close : function (elem, wait) {
          // Unary Plus: +"2" === 2
          var timer = (wait && !isNaN(wait)) ? +wait : this.delay,
              self  = this,
              hideElement, transitionDone;

          // set click event on log messages
          this.bind(elem, "click", function () {
            hideElement(elem);
          });
          // Hide the dialog box after transition
          // This ensure it doens't block any element from being clicked
          transitionDone = function (event) {
            event.stopPropagation();
            // unbind event so function only gets called once
            self.unbind(this, self.transition.type, transitionDone);
            // remove log message
            elLog.removeChild(this);
            if (!elLog.hasChildNodes()) elLog.className += " alertify-logs-hidden";
          };
          // this sets the hide class to transition out
          // or removes the child if css transitions aren't supported
          hideElement = function (el) {
            // ensure element exists
            if (typeof el !== "undefined" && el.parentNode === elLog) {
              // whether CSS transition exists
              if (self.transition.supported) {
                self.bind(el, self.transition.type, transitionDone);
                el.className += " alertify-log-hide";
              } else {
                elLog.removeChild(el);
                if (!elLog.hasChildNodes()) elLog.className += " alertify-logs-hidden";
              }
            }
          };
          // never close (until click) if wait is set to 0
          if (wait === 0) return;
          // set timeout to auto close the log message
          setTimeout(function () { hideElement(elem); }, timer);
        },

        /**
         * Create a dialog box
         *
         * @param  {String}   message        The message passed from the callee
         * @param  {String}   type           Type of dialog to create
         * @param  {Function} fn             [Optional] Callback function
         * @param  {String}   placeholder    [Optional] Default value for prompt input field
         * @param  {String}   cssClass       [Optional] Class(es) to append to dialog box
         *
         * @return {Object}
         */
        dialog : function (message, type, fn, placeholder, cssClass) {
          // set the current active element
          // this allows the keyboard focus to be resetted
          // after the dialog box is closed
          elCallee = document.activeElement;
          // check to ensure the alertify dialog element
          // has been successfully created
          var check = function () {
            if ((elLog && elLog.scrollTop !== null) && (elCover && elCover.scrollTop !== null)) return;
            else check();
          };
          // error catching
          if (typeof message !== "string") throw new Error("message must be a string");
          if (typeof type !== "string") throw new Error("type must be a string");
          if (typeof fn !== "undefined" && typeof fn !== "function") throw new Error("fn must be a function");
          // initialize alertify if it hasn't already been done
          this.init();
          check();

          queue.push({ type: type, message: message, callback: fn, placeholder: placeholder, cssClass: cssClass });
          if (!isopen) this.setup();

          return this;
        },

        /**
         * Extend the log method to create custom methods
         *
         * @param  {String} type    Custom method name
         *
         * @return {Function}
         */
        extend : function (type) {
          if (typeof type !== "string") throw new Error("extend method must have exactly one paramter");
          return function (message, wait) {
            this.log(message, type, wait);
            return this;
          };
        },

        /**
         * Hide the dialog and rest to defaults
         *
         * @return {undefined}
         */
        hide : function () {
          var transitionDone,
              self = this;
          // remove reference from queue
          queue.splice(0,1);
          // if items remaining in the queue
          if (queue.length > 0) this.setup(true);
          else {
            isopen = false;
            // Hide the dialog box after transition
            // This ensure it doens't block any element from being clicked
            transitionDone = function (event) {
              event.stopPropagation();
              // unbind event so function only gets called once
              self.unbind(elDialog, self.transition.type, transitionDone);
            };
            // whether CSS transition exists
            if (this.transition.supported) {
              this.bind(elDialog, this.transition.type, transitionDone);
              elDialog.className = "alertify alertify-hide alertify-hidden";
            } else {
              elDialog.className = "alertify alertify-hide alertify-hidden alertify-isHidden";
            }
            elCover.className  = "alertify-cover alertify-cover-hidden";
            // set focus to the last element or body
            // after the dialog is closed
            elCallee.focus();
          }
        },

        /**
         * Initialize Alertify
         * Create the 2 main elements
         *
         * @return {undefined}
         */
        init : function () {
          // ensure legacy browsers support html5 tags
          document.createElement("nav");
          document.createElement("article");
          document.createElement("section");
          // cover
          if ($("alertify-cover") == null) {
            elCover = document.createElement("div");
            elCover.setAttribute("id", "alertify-cover");
            elCover.className = "alertify-cover alertify-cover-hidden";
            document.body.appendChild(elCover);
          }
          // main element
          if ($("alertify") == null) {
            isopen = false;
            queue = [];
            elDialog = document.createElement("section");
            elDialog.setAttribute("id", "alertify");
            elDialog.className = "alertify alertify-hidden";
            document.body.appendChild(elDialog);
          }
          // log element
          if ($("alertify-logs") == null) {
            elLog = document.createElement("section");
            elLog.setAttribute("id", "alertify-logs");
            elLog.className = "alertify-logs alertify-logs-hidden";
            document.body.appendChild(elLog);
          }
          // set tabindex attribute on body element
          // this allows script to give it focus
          // after the dialog is closed
          document.body.setAttribute("tabindex", "0");
          // set transition type
          this.transition = getTransitionEvent();
        },

        /**
         * Show a new log message box
         *
         * @param  {String} message    The message passed from the callee
         * @param  {String} type       [Optional] Optional type of log message
         * @param  {Number} wait       [Optional] Time (in ms) to wait before auto-hiding the log
         *
         * @return {Object}
         */
        log : function (message, type, wait) {
          // check to ensure the alertify dialog element
          // has been successfully created
          var check = function () {
            if (elLog && elLog.scrollTop !== null) return;
            else check();
          };
          // initialize alertify if it hasn't already been done
          this.init();
          check();

          elLog.className = "alertify-logs";
          this.notify(message, type, wait);
          return this;
        },

        /**
         * Add new log message
         * If a type is passed, a class name "alertify-log-{type}" will get added.
         * This allows for custom look and feel for various types of notifications.
         *
         * @param  {String} message    The message passed from the callee
         * @param  {String} type       [Optional] Type of log message
         * @param  {Number} wait       [Optional] Time (in ms) to wait before auto-hiding
         *
         * @return {undefined}
         */
        notify : function (message, type, wait) {
          var log = document.createElement("article");
          log.className = "alertify-log" + ((typeof type === "string" && type !== "") ? " alertify-log-" + type : "");
          log.innerHTML = message;
          // append child
          elLog.appendChild(log);
          // triggers the CSS animation
          setTimeout(function() { log.className = log.className + " alertify-log-show"; }, 50);
          this.close(log, wait);
        },

        /**
         * Set properties
         *
         * @param {Object} args     Passing parameters
         *
         * @return {undefined}
         */
        set : function (args) {
          var k;
          // error catching
          if (typeof args !== "object" && args instanceof Array) throw new Error("args must be an object");
          // set parameters
          for (k in args) {
            if (args.hasOwnProperty(k)) {
              this[k] = args[k];
            }
          }
        },

        /**
         * Common place to set focus to proper element
         *
         * @return {undefined}
         */
        setFocus : function () {
          if (input) {
            input.focus();
            input.select();
          }
          else btnFocus.focus();
        },

        /**
         * Initiate all the required pieces for the dialog box
         *
         * @return {undefined}
         */
        setup : function (fromQueue) {
          var item = queue[0],
              self = this,
              transitionDone;

          // dialog is open
          isopen = true;
          // Set button focus after transition
          transitionDone = function (event) {
            event.stopPropagation();
            self.setFocus();
            // unbind event so function only gets called once
            self.unbind(elDialog, self.transition.type, transitionDone);
          };
          // whether CSS transition exists
          if (this.transition.supported && !fromQueue) {
            this.bind(elDialog, this.transition.type, transitionDone);
          }
          // build the proper dialog HTML
          elDialog.innerHTML = this.build(item);
          // assign all the common elements
          btnReset  = $("alertify-resetFocus");
          btnResetBack  = $("alertify-resetFocusBack");
          btnOK     = $("alertify-ok")     || undefined;
          btnCancel = $("alertify-cancel") || undefined;
          btnFocus  = (_alertify.buttonFocus === "cancel") ? btnCancel : ((_alertify.buttonFocus === "none") ? $("alertify-noneFocus") : btnOK),
          input     = $("alertify-text")   || undefined;
          form      = $("alertify-form")   || undefined;
          // add placeholder value to the input field
          if (typeof item.placeholder === "string" && item.placeholder !== "") input.value = item.placeholder;
          if (fromQueue) this.setFocus();
          this.addListeners(item.callback);
        },

        /**
         * Unbind events to elements
         *
         * @param  {Object}   el       HTML Object
         * @param  {Event}    event    Event to detach to element
         * @param  {Function} fn       Callback function
         *
         * @return {undefined}
         */
        unbind : function (el, event, fn) {
          if (typeof el.removeEventListener === "function") {
            el.removeEventListener(event, fn, false);
          } else if (el.detachEvent) {
            el.detachEvent("on" + event, fn);
          }
        }
      };

      return {
        alert   : function (message, fn, cssClass) { _alertify.dialog(message, "alert", fn, "", cssClass); return this; },
        confirm : function (message, fn, cssClass) { _alertify.dialog(message, "confirm", fn, "", cssClass); return this; },
        extend  : _alertify.extend,
        init    : _alertify.init,
        log     : function (message, type, wait) { _alertify.log(message, type, wait); return this; },
        prompt  : function (message, fn, placeholder, cssClass) { _alertify.dialog(message, "prompt", fn, placeholder, cssClass); return this; },
        success : function (message, wait) { _alertify.log(message, "success", wait); return this; },
        error   : function (message, wait) { _alertify.log(message, "error", wait); return this; },
        set     : function (args) { _alertify.set(args); },
        labels  : _alertify.labels,
        debug   : _alertify.handleErrors
      };
    };

    // AMD and window support
    if (typeof define === "function") {
      define([], function () { return new Alertify(); });
    } else if (typeof global.alertify === "undefined") {
      global.alertify = new Alertify();
    }

  }(this));


/* pickadate.js v3.3.0, 2013/10/13
 * By Amsul, http://amsul.ca
 * Hosted on http://amsul.github.io/pickadate.js
 * Licensed under MIT
 */

  /*jshint
     debug: true,
     devel: true,
     browser: true,
     asi: true,
     unused: true,
     boss: true,
     eqnull: true
   */

  (function ( factory ) {

      // Register as an anonymous module.
      if ( typeof define === 'function' && define.amd )
          define( 'picker', ['jquery'], factory )

      // Or using browser globals.
      else this.Picker = factory( jQuery )

  }(function( $ ) {

  var $document = $( document )


  /**
   * The picker constructor that creates a blank picker.
   */
  function PickerConstructor( ELEMENT, NAME, COMPONENT, OPTIONS ) {

      // If there’s no element, return the picker constructor.
      if ( !ELEMENT ) return PickerConstructor


      var
          // The state of the picker.
          STATE = {
              id: Math.abs( ~~( Math.random() * 1e9 ) )
          },


          // Merge the defaults and options passed.
          SETTINGS = COMPONENT ? $.extend( true, {}, COMPONENT.defaults, OPTIONS ) : OPTIONS || {},


          // Merge the default classes with the settings classes.
          CLASSES = $.extend( {}, PickerConstructor.klasses(), SETTINGS.klass ),


          // The element node wrapper into a jQuery object.
          $ELEMENT = $( ELEMENT ),


          // Pseudo picker constructor.
          PickerInstance = function() {
              return this.start()
          },


          // The picker prototype.
          P = PickerInstance.prototype = {

              constructor: PickerInstance,

              $node: $ELEMENT,


              /**
               * Initialize everything
               */
              start: function() {

                  // If it’s already started, do nothing.
                  if ( STATE && STATE.start ) return P


                  // Update the picker states.
                  STATE.methods = {}
                  STATE.start = true
                  STATE.open = false
                  STATE.type = ELEMENT.type


                  // Confirm focus state, convert into text input to remove UA stylings,
                  // and set as readonly to prevent keyboard popup.
                  ELEMENT.autofocus = ELEMENT == document.activeElement
                  ELEMENT.type = 'text'
                  ELEMENT.readOnly = true


                  // Create a new picker component with the settings.
                  P.component = new COMPONENT( P, SETTINGS )


                  // Create the picker root with a new wrapped holder and bind the events.
                  P.$root = $( PickerConstructor._.node( 'div', createWrappedComponent(), CLASSES.picker ) ).
                      on({

                          // When something within the root is focused, stop from bubbling
                          // to the doc and remove the “focused” state from the root.
                          focusin: function( event ) {
                              P.$root.removeClass( CLASSES.focused )
                              event.stopPropagation()
                          },

                          // If the click is not on the root holder, stop it from bubbling to the doc.
                          'mousedown click': function( event ) {
                              if ( event.target != P.$root.children()[ 0 ] ) {
                                  event.stopPropagation()
                              }
                          }
                      }).

                      // If there’s a click on an actionable element, carry out the actions.
                      on( 'click', '[data-pick], [data-nav], [data-clear]', function() {

                          var $target = $( this ),
                              targetData = $target.data(),
                              targetDisabled = $target.hasClass( CLASSES.navDisabled ) || $target.hasClass( CLASSES.disabled ),

                              // * For IE, non-focusable elements can be active elements as well
                              //   (http://stackoverflow.com/a/2684561).
                              activeElement = document.activeElement
                              activeElement = activeElement && ( activeElement.type || activeElement.href )

                          // If it’s disabled or nothing inside is actively focused, re-focus the element.
                          if ( targetDisabled || !$.contains( P.$root[0], activeElement ) ) {
                              ELEMENT.focus()
                          }

                          // If something is superficially changed, update the `highlight` based on the `nav`.
                          if ( targetData.nav && !targetDisabled ) {
                              P.set( 'highlight', P.component.item.highlight, { nav: targetData.nav } )
                          }

                          // If something is picked, set `select` then close with focus.
                          else if ( PickerConstructor._.isInteger( targetData.pick ) && !targetDisabled ) {
                              P.set( 'select', targetData.pick ).close( true )
                          }

                          // If a “clear” button is pressed, empty the values and close with focus.
                          else if ( targetData.clear ) {
                              P.clear().close( true )
                          }
                      }) //P.$root


                  // If there’s a format for the hidden input element, create the element.
                  if ( SETTINGS.formatSubmit ) {

                      P._hidden = $(
                          '<input ' +
                          'type=hidden ' +

                          // Create the name by using the original input plus a prefix and suffix.
                          'name="' + ( typeof SETTINGS.hiddenPrefix == 'string' ? SETTINGS.hiddenPrefix : '' ) +
                              ELEMENT.name +
                              ( typeof SETTINGS.hiddenSuffix == 'string' ? SETTINGS.hiddenSuffix : '_submit' ) +
                          '"' +

                          // If the element has a `data-value`, set the element `value` as well.
                          ( $ELEMENT.data( 'value' ) ?
                              ' value="' + PickerConstructor._.trigger( P.component.formats.toString, P.component, [ SETTINGS.formatSubmit, P.component.item.select ] ) + '"' :
                              ''
                          ) +
                          '>'
                      )[ 0 ]
                  }


                  // Add the class and bind the events on the element.
                  $ELEMENT.addClass( CLASSES.input ).

                      // On focus/click, open the picker and adjust the root “focused” state.
                      on( 'focus.P' + STATE.id + ' click.P' + STATE.id, focusToOpen ).

                      // If the value changes, update the hidden input with the correct format.
                      on( 'change.P' + STATE.id, function() {
                          if ( P._hidden ) {
                              P._hidden.value = ELEMENT.value ? PickerConstructor._.trigger( P.component.formats.toString, P.component, [ SETTINGS.formatSubmit, P.component.item.select ] ) : ''
                          }
                      }).

                      // Handle keyboard event based on the picker being opened or not.
                      on( 'keydown.P' + STATE.id, function( event ) {

                          var keycode = event.keyCode,

                              // Check if one of the delete keys was pressed.
                              isKeycodeDelete = /^(8|46)$/.test( keycode )

                          // For some reason IE clears the input value on “escape”.
                          if ( keycode == 27 ) {
                              P.close()
                              return false
                          }

                          // Check if `space` or `delete` was pressed or the picker is closed with a key movement.
                          if ( keycode == 32 || isKeycodeDelete || !STATE.open && P.component.key[ keycode ] ) {

                              // Prevent it from moving the page and bubbling to doc.
                              event.preventDefault()
                              event.stopPropagation()

                              // If `delete` was pressed, clear the values and close the picker.
                              // Otherwise open the picker.
                              if ( isKeycodeDelete ) { P.clear().close() }
                              else { P.open() }
                          }
                      }).

                      // If there’s a `data-value`, update the value of the element.
                      val( $ELEMENT.data( 'value' ) ? PickerConstructor._.trigger( P.component.formats.toString, P.component, [ SETTINGS.format, P.component.item.select ] ) : ELEMENT.value ).

                      // Insert the hidden input after the element.
                      after( P._hidden ).

                      // Store the picker data by component name.
                      data( NAME, P )


                  // Insert the root as specified in the settings.
                  if ( SETTINGS.container ) $( SETTINGS.container ).append( P.$root )
                  else $ELEMENT.after( P.$root )


                  // Bind the default component and settings events.
                  P.on({
                      start: P.component.onStart,
                      render: P.component.onRender,
                      stop: P.component.onStop,
                      open: P.component.onOpen,
                      close: P.component.onClose,
                      set: P.component.onSet
                  }).on({
                      start: SETTINGS.onStart,
                      render: SETTINGS.onRender,
                      stop: SETTINGS.onStop,
                      open: SETTINGS.onOpen,
                      close: SETTINGS.onClose,
                      set: SETTINGS.onSet
                  })


                  // If the element has autofocus, open the picker.
                  if ( ELEMENT.autofocus ) {
                      P.open()
                  }


                  // Trigger queued the “start” and “render” events.
                  return P.trigger( 'start' ).trigger( 'render' )
              }, //start


              /**
               * Render a new picker
               */
              render: function( entireComponent ) {

                  // Insert a new component holder in the root or box.
                  if ( entireComponent ) P.$root.html( createWrappedComponent() )
                  else P.$root.find( '.' + CLASSES.box ).html( P.component.nodes( STATE.open ) )

                  // Trigger the queued “render” events.
                  return P.trigger( 'render' )
              }, //render


              /**
               * Destroy everything
               */
              stop: function() {

                  // If it’s already stopped, do nothing.
                  if ( !STATE.start ) return P

                  // Then close the picker.
                  P.close()

                  // Remove the hidden field.
                  if ( P._hidden ) {
                      P._hidden.parentNode.removeChild( P._hidden )
                  }

                  // Remove the root.
                  P.$root.remove()

                  // Remove the input class, unbind the events, and remove the stored data.
                  $ELEMENT.removeClass( CLASSES.input ).off( '.P' + STATE.id ).removeData( NAME )

                  // Restore the element state
                  ELEMENT.type = STATE.type
                  ELEMENT.readOnly = false

                  // Trigger the queued “stop” events.
                  P.trigger( 'stop' )

                  // Reset the picker states.
                  STATE.methods = {}
                  STATE.start = false

                  return P
              }, //stop


              /*
               * Open up the picker
               */
              open: function( dontGiveFocus ) {

                  // If it’s already open, do nothing.
                  if ( STATE.open ) return P

                  // Add the “active” class.
                  $ELEMENT.addClass( CLASSES.active )

                  // Add the “opened” class to the picker root.
                  P.$root.addClass( CLASSES.opened )

                  // If we have to give focus, bind the element and doc events.
                  if ( dontGiveFocus !== false ) {

                      // Set it as open.
                      STATE.open = true

                      // Pass focus to the element’s jQuery object.
                      $ELEMENT.trigger( 'focus' )

                      // Bind the document events.
                      $document.on( 'click.P' + STATE.id + ' focusin.P' + STATE.id, function( event ) {

                          // If the target of the event is not the element, close the picker picker.
                          // * Don’t worry about clicks or focusins on the root because those don’t bubble up.
                          //   Also, for Firefox, a click on an `option` element bubbles up directly
                          //   to the doc. So make sure the target wasn't the doc.
                          if ( event.target != ELEMENT && event.target != document ) P.close()

                      }).on( 'keydown.P' + STATE.id, function( event ) {

                          var
                              // Get the keycode.
                              keycode = event.keyCode,

                              // Translate that to a selection change.
                              keycodeToMove = P.component.key[ keycode ],

                              // Grab the target.
                              target = event.target


                          // On escape, close the picker and give focus.
                          if ( keycode == 27 ) {
                              P.close( true )
                          }


                          // Check if there is a key movement or “enter” keypress on the element.
                          else if ( target == ELEMENT && ( keycodeToMove || keycode == 13 ) ) {

                              // Prevent the default action to stop page movement.
                              event.preventDefault()

                              // Trigger the key movement action.
                              if ( keycodeToMove ) {
                                  PickerConstructor._.trigger( P.component.key.go, P, [ PickerConstructor._.trigger( keycodeToMove ) ] )
                              }

                              // On “enter”, if the highlighted item isn’t disabled, set the value and close.
                              else if ( !P.$root.find( '.' + CLASSES.highlighted ).hasClass( CLASSES.disabled ) ) {
                                  P.set( 'select', P.component.item.highlight ).close()
                              }
                          }


                          // If the target is within the root and “enter” is pressed,
                          // prevent the default action and trigger a click on the target instead.
                          else if ( $.contains( P.$root[0], target ) && keycode == 13 ) {
                              event.preventDefault()
                              target.click()
                          }
                      })
                  }

                  // Trigger the queued “open” events.
                  return P.trigger( 'open' )
              }, //open


              /**
               * Close the picker
               */
              close: function( giveFocus ) {

                  // If we need to give focus, do it before changing states.
                  if ( giveFocus ) {
                      // ....ah yes! It would’ve been incomplete without a crazy workaround for IE :|
                      // The focus is triggered *after* the close has completed - causing it
                      // to open again. So unbind and rebind the event at the next tick.
                      $ELEMENT.off( 'focus.P' + STATE.id ).trigger( 'focus' )
                      setTimeout( function() {
                          $ELEMENT.on( 'focus.P' + STATE.id, focusToOpen )
                      }, 0 )
                  }

                  // Remove the “active” class.
                  $ELEMENT.removeClass( CLASSES.active )

                  // Remove the “opened” and “focused” class from the picker root.
                  P.$root.removeClass( CLASSES.opened + ' ' + CLASSES.focused )

                  // If it’s open, update the state.
                  if ( STATE.open ) {

                      // Set it as closed.
                      STATE.open = false

                      // Unbind the document events.
                      $document.off( '.P' + STATE.id )
                  }

                  // Trigger the queued “close” events.
                  return P.trigger( 'close' )
              }, //close


              /**
               * Clear the values
               */
              clear: function() {
                  return P.set( 'clear' )
              }, //clear


              /**
               * Set something
               */
              set: function( thing, value, options ) {

                  var thingItem, thingValue,
                      thingIsObject = PickerConstructor._.isObject( thing ),
                      thingObject = thingIsObject ? thing : {}

                  if ( thing ) {

                      // If the thing isn’t an object, make it one.
                      if ( !thingIsObject ) {
                          thingObject[ thing ] = value
                      }

                      // Go through the things of items to set.
                      for ( thingItem in thingObject ) {

                          // Grab the value of the thing.
                          thingValue = thingObject[ thingItem ]

                          // First, if the item exists and there’s a value, set it.
                          if ( P.component.item[ thingItem ] ) {
                              P.component.set( thingItem, thingValue, options || {} )
                          }

                          // Then, check to update the element value and broadcast a change.
                          if ( thingItem == 'select' || thingItem == 'clear' ) {
                              $ELEMENT.val( thingItem == 'clear' ? '' :
                                  PickerConstructor._.trigger( P.component.formats.toString, P.component, [ SETTINGS.format, P.component.get( thingItem ) ] )
                              ).trigger( 'change' )
                          }
                      }

                      // Render a new picker.
                      P.render()
                  }

                  // Trigger queued “set” events and pass the `thingObject`.
                  return P.trigger( 'set', thingObject )
              }, //set


              /**
               * Get something
               */
              get: function( thing, format ) {

                  // Make sure there’s something to get.
                  thing = thing || 'value'

                  // If a picker state exists, return that.
                  if ( STATE[ thing ] != null ) {
                      return STATE[ thing ]
                  }

                  // Return the value, if that.
                  if ( thing == 'value' ) {
                      return ELEMENT.value
                  }

                  // Check if a component item exists, return that.
                  if ( P.component.item[ thing ] ) {
                      if ( typeof format == 'string' ) {
                          return PickerConstructor._.trigger( P.component.formats.toString, P.component, [ format, P.component.get( thing ) ] )
                      }
                      return P.component.get( thing )
                  }
              }, //get



              /**
               * Bind events on the things.
               */
              on: function( thing, method ) {

                  var thingName, thingMethod,
                      thingIsObject = PickerConstructor._.isObject( thing ),
                      thingObject = thingIsObject ? thing : {}

                  if ( thing ) {

                      // If the thing isn’t an object, make it one.
                      if ( !thingIsObject ) {
                          thingObject[ thing ] = method
                      }

                      // Go through the things to bind to.
                      for ( thingName in thingObject ) {

                          // Grab the method of the thing.
                          thingMethod = thingObject[ thingName ]

                          // Make sure the thing methods collection exists.
                          STATE.methods[ thingName ] = STATE.methods[ thingName ] || []

                          // Add the method to the relative method collection.
                          STATE.methods[ thingName ].push( thingMethod )
                      }
                  }

                  return P
              }, //on


              /**
               * Fire off method events.
               */
              trigger: function( name, data ) {
                  var methodList = STATE.methods[ name ]
                  if ( methodList ) {
                      methodList.map( function( method ) {
                          PickerConstructor._.trigger( method, P, [ data ] )
                      })
                  }
                  return P
              } //trigger
          } //PickerInstance.prototype


      /**
       * Wrap the picker holder components together.
       */
      function createWrappedComponent() {

          // Create a picker wrapper holder
          return PickerConstructor._.node( 'div',

              // Create a picker wrapper node
              PickerConstructor._.node( 'div',

                  // Create a picker frame
                  PickerConstructor._.node( 'div',

                      // Create a picker box node
                      PickerConstructor._.node( 'div',

                          // Create the components nodes.
                          P.component.nodes( STATE.open ),

                          // The picker box class
                          CLASSES.box
                      ),

                      // Picker wrap class
                      CLASSES.wrap
                  ),

                  // Picker frame class
                  CLASSES.frame
              ),

              // Picker holder class
              CLASSES.holder
          ) //endreturn
      } //createWrappedComponent


      // Separated for IE
      function focusToOpen( event ) {

          // Stop the event from propagating to the doc.
          event.stopPropagation()

          // If it’s a focus event, add the “focused” class to the root.
          if ( event.type == 'focus' ) P.$root.addClass( CLASSES.focused )

          // And then finally open the picker.
          P.open()
      }


      // Return a new picker instance.
      return new PickerInstance()
  } //PickerConstructor



  /**
   * The default classes and prefix to use for the HTML classes.
   */
  PickerConstructor.klasses = function( prefix ) {
      prefix = prefix || 'picker'
      return {

          picker: prefix,
          opened: prefix + '--opened',
          focused: prefix + '--focused',

          input: prefix + '__input',
          active: prefix + '__input--active',

          holder: prefix + '__holder',

          frame: prefix + '__frame',
          wrap: prefix + '__wrap',

          box: prefix + '__box'
      }
  } //PickerConstructor.klasses



  /**
   * PickerConstructor helper methods.
   */
  PickerConstructor._ = {

      /**
       * Create a group of nodes. Expects:
       * `
          {
              min:    {Integer},
              max:    {Integer},
              i:      {Integer},
              node:   {String},
              item:   {Function}
          }
       * `
       */
      group: function( groupObject ) {

          var
              // Scope for the looped object
              loopObjectScope,

              // Create the nodes list
              nodesList = '',

              // The counter starts from the `min`
              counter = PickerConstructor._.trigger( groupObject.min, groupObject )


          // Loop from the `min` to `max`, incrementing by `i`
          for ( ; counter <= PickerConstructor._.trigger( groupObject.max, groupObject, [ counter ] ); counter += groupObject.i ) {

              // Trigger the `item` function within scope of the object
              loopObjectScope = PickerConstructor._.trigger( groupObject.item, groupObject, [ counter ] )

              // Splice the subgroup and create nodes out of the sub nodes
              nodesList += PickerConstructor._.node(
                  groupObject.node,
                  loopObjectScope[ 0 ],   // the node
                  loopObjectScope[ 1 ],   // the classes
                  loopObjectScope[ 2 ]    // the attributes
              )
          }

          // Return the list of nodes
          return nodesList
      }, //group


      /**
       * Create a dom node string
       */
      node: function( wrapper, item, klass, attribute ) {

          // If the item is false-y, just return an empty string
          if ( !item ) return ''

          // If the item is an array, do a join
          item = $.isArray( item ) ? item.join( '' ) : item

          // Check for the class
          klass = klass ? ' class="' + klass + '"' : ''

          // Check for any attributes
          attribute = attribute ? ' ' + attribute : ''

          // Return the wrapped item
          return '<' + wrapper + klass + attribute + '>' + item + '</' + wrapper + '>'
      }, //node


      /**
       * Lead numbers below 10 with a zero.
       */
      lead: function( number ) {
          return ( number < 10 ? '0': '' ) + number
      },


      /**
       * Trigger a function otherwise return the value.
       */
      trigger: function( callback, scope, args ) {
          return typeof callback == 'function' ? callback.apply( scope, args || [] ) : callback
      },


      /**
       * If the second character is a digit, length is 2 otherwise 1.
       */
      digits: function( string ) {
          return ( /\d/ ).test( string[ 1 ] ) ? 2 : 1
      },


      /**
       * Tell if something is an object.
       */
      isObject: function( value ) {
          return {}.toString.call( value ).indexOf( 'Object' ) > -1
      },


      /**
       * Tell if something is a date object.
       */
      isDate: function( value ) {
          return {}.toString.call( value ).indexOf( 'Date' ) > -1 && this.isInteger( value.getDate() )
      },


      /**
       * Tell if something is an integer.
       */
      isInteger: function( value ) {
          return {}.toString.call( value ).indexOf( 'Number' ) > -1 && value % 1 === 0
      }
  } //PickerConstructor._



  /**
   * Extend the picker with a component and defaults.
   */
  PickerConstructor.extend = function( name, Component ) {

      // Extend jQuery.
      $.fn[ name ] = function( options, action ) {

          // Grab the component data.
          var componentData = this.data( name )

          // If the picker is requested, return the data object.
          if ( options == 'picker' ) {
              return componentData
          }

          // If the component data exists and `options` is a string, carry out the action.
          if ( componentData && typeof options == 'string' ) {
              PickerConstructor._.trigger( componentData[ options ], componentData, [ action ] )
              return this
          }

          // Otherwise go through each matched element and if the component
          // doesn’t exist, create a new picker using `this` element
          // and merging the defaults and options with a deep copy.
          return this.each( function() {
              var $this = $( this )
              if ( !$this.data( name ) ) {
                  new PickerConstructor( this, name, Component, options )
              }
          })
      }

      // Set the defaults.
      $.fn[ name ].defaults = Component.defaults
  } //PickerConstructor.extend



  // Expose the picker constructor.
  return PickerConstructor


  }));


/* Date picker for pickadate.js v3.3.0
 * http://amsul.github.io/pickadate.js/date.htm
 */

    /*jshint
       debug: true,
       devel: true,
       browser: true,
       asi: true,
       unused: true,
       boss: true
     */

    (function ( factory ) {

        // Register as an anonymous module.
        if ( typeof define === 'function' && define.amd )
            define( ['picker','jquery'], factory )

        // Or using browser globals.
        else factory( Picker, jQuery )

    }(function( Picker, $ ) {


    /**
     * Globals and constants
     */
    var DAYS_IN_WEEK = 7,
        WEEKS_IN_CALENDAR = 6



    /**
     * The date picker constructor
     */
    function DatePicker( picker, settings ) {

        var calendar = this,
            elementValue = picker.$node[ 0 ].value,
            elementDataValue = picker.$node.data( 'value' ),
            valueString = elementDataValue || elementValue,
            formatString = elementDataValue ? settings.formatSubmit : settings.format,
            isRTL = function() {
                return getComputedStyle( picker.$root[0] ).direction === 'rtl'
            }

        calendar.settings = settings

        // The queue of methods that will be used to build item objects.
        calendar.queue = {
            min: 'measure create',
            max: 'measure create',
            now: 'now create',
            select: 'parse create validate',
            highlight: 'navigate create validate',
            view: 'create validate viewset',
            disable: 'flipItem',
            enable: 'flipItem'
        }

        // The component's item object.
        calendar.item = {}

        calendar.item.disable = ( settings.disable || [] ).slice( 0 )
        calendar.item.enable = -(function( collectionDisabled ) {
            return collectionDisabled[ 0 ] === true ? collectionDisabled.shift() : -1
        })( calendar.item.disable )

        calendar.
            set( 'min', settings.min ).
            set( 'max', settings.max ).
            set( 'now' ).

            // Setting the `select` also sets the `highlight` and `view`.
            set( 'select',

                // Use the value provided or default to selecting “today”.
                valueString || calendar.item.now,
                {
                    // Use the appropriate format.
                    format: formatString,

                    // Set user-provided month data as true when there is a
                    // “mm” or “m” used in the relative format string.
                    data: (function( formatArray ) {
                        return valueString && ( formatArray.indexOf( 'mm' ) > -1 || formatArray.indexOf( 'm' ) > -1 )
                    })( calendar.formats.toArray( formatString ) )
                }
            )


        // The keycode to movement mapping.
        calendar.key = {
            40: 7, // Down
            38: -7, // Up
            39: function() { return isRTL() ? -1 : 1 }, // Right
            37: function() { return isRTL() ? 1 : -1 }, // Left
            go: function( timeChange ) {
                calendar.set( 'highlight', [ calendar.item.highlight.year, calendar.item.highlight.month, calendar.item.highlight.date + timeChange ], { interval: timeChange } )
                this.render()
            }
        }


        // Bind some picker events.
        picker.
            on( 'render', function() {
                picker.$root.find( '.' + settings.klass.selectMonth ).on( 'change', function() {
                    picker.set( 'highlight', [ picker.get( 'view' ).year, this.value, picker.get( 'highlight' ).date ] )
                    picker.$root.find( '.' + settings.klass.selectMonth ).trigger( 'focus' )
                })
                picker.$root.find( '.' + settings.klass.selectYear ).on( 'change', function() {
                    picker.set( 'highlight', [ this.value, picker.get( 'view' ).month, picker.get( 'highlight' ).date ] )
                    picker.$root.find( '.' + settings.klass.selectYear ).trigger( 'focus' )
                })
            }).
            on( 'open', function() {
                picker.$root.find( 'button, select' ).attr( 'disabled', false )
            }).
            on( 'close', function() {
                picker.$root.find( 'button, select' ).attr( 'disabled', true )
            })

    } //DatePicker


    /**
     * Set a datepicker item object.
     */
    DatePicker.prototype.set = function( type, value, options ) {

        var calendar = this

        // Go through the queue of methods, and invoke the function. Update this
        // as the time unit, and set the final resultant as this item type.
        // * In the case of `enable`, keep the queue but set `disable` instead.
        //   And in the case of `flip`, keep the queue but set `enable` instead.
        calendar.item[ ( type == 'enable' ? 'disable' : type == 'flip' ? 'enable' : type ) ] = calendar.queue[ type ].split( ' ' ).map( function( method ) {
            return value = calendar[ method ]( type, value, options )
        }).pop()

        // Check if we need to cascade through more updates.
        if ( type == 'select' ) {
            calendar.set( 'highlight', calendar.item.select, options )
        }
        else if ( type == 'highlight' ) {
            calendar.set( 'view', calendar.item.highlight, options )
        }
        else if ( ( type == 'flip' || type == 'min' || type == 'max' || type == 'disable' || type == 'enable' ) && calendar.item.select && calendar.item.highlight ) {
            calendar.
                set( 'select', calendar.item.select, options ).
                set( 'highlight', calendar.item.highlight, options )
        }

        return calendar
    } //DatePicker.prototype.set


    /**
     * Get a datepicker item object.
     */
    DatePicker.prototype.get = function( type ) {
        return this.item[ type ]
    } //DatePicker.prototype.get


    /**
     * Create a picker date object.
     */
    DatePicker.prototype.create = function( type, value, options ) {

        var isInfiniteValue,
            calendar = this

        // If there’s no value, use the type as the value.
        value = value === undefined ? type : value


        // If it’s infinity, update the value.
        if ( value == -Infinity || value == Infinity ) {
            isInfiniteValue = value
        }

        // If it’s an object, use the native date object.
        else if ( Picker._.isObject( value ) && Picker._.isInteger( value.pick ) ) {
            value = value.obj
        }

        // If it’s an array, convert it into a date and make sure
        // that it’s a valid date – otherwise default to today.
        else if ( $.isArray( value ) ) {
            value = new Date( value[ 0 ], value[ 1 ], value[ 2 ] )
            value = Picker._.isDate( value ) ? value : calendar.create().obj
        }

        // If it’s a number or date object, make a normalized date.
        else if ( Picker._.isInteger( value ) || Picker._.isDate( value ) ) {
            value = calendar.normalize( new Date( value ), options )
        }

        // If it’s a literal true or any other case, set it to now.
        else /*if ( value === true )*/ {
            value = calendar.now( type, value, options )
        }

        // Return the compiled object.
        return {
            year: isInfiniteValue || value.getFullYear(),
            month: isInfiniteValue || value.getMonth(),
            date: isInfiniteValue || value.getDate(),
            day: isInfiniteValue || value.getDay(),
            obj: isInfiniteValue || value,
            pick: isInfiniteValue || value.getTime()
        }
    } //DatePicker.prototype.create


    /**
     * Get the date today.
     */
    DatePicker.prototype.now = function( type, value, options ) {
        value = new Date()
        if ( options && options.rel ) {
            value.setDate( value.getDate() + options.rel )
        }
        return this.normalize( value, options )
    } //DatePicker.prototype.now


    /**
     * Navigate to next/prev month.
     */
    DatePicker.prototype.navigate = function( type, value, options ) {

        if ( Picker._.isObject( value ) ) {

            var targetDateObject = new Date( value.year, value.month + ( options && options.nav ? options.nav : 0 ), 1 ),
                year = targetDateObject.getFullYear(),
                month = targetDateObject.getMonth(),
                date = value.date

            // Make sure the date is valid and if the month we’re going to doesn’t have enough
            // days, keep decreasing the date until we reach the month’s last date.
            while ( Picker._.isDate( targetDateObject ) && new Date( year, month, date ).getMonth() !== month ) {
                date -= 1
            }

            value = [ year, month, date ]
        }

        return value
    } //DatePicker.prototype.navigate


    /**
     * Normalize a date by setting the hours to midnight.
     */
    DatePicker.prototype.normalize = function( value/*, options*/ ) {
        value.setHours( 0, 0, 0, 0 )
        return value
    }


    /**
     * Measure the range of dates.
     */
    DatePicker.prototype.measure = function( type, value/*, options*/ ) {

        var calendar = this

        // If it's anything false-y, remove the limits.
        if ( !value ) {
            value = type == 'min' ? -Infinity : Infinity
        }

        // If it's an integer, get a date relative to today.
        else if ( Picker._.isInteger( value ) ) {
            value = calendar.now( type, value, { rel: value } )
        }

        return value
    } ///DatePicker.prototype.measure


    /**
     * Create a viewset object based on navigation.
     */
    DatePicker.prototype.viewset = function( type, dateObject/*, options*/ ) {
        return this.create([ dateObject.year, dateObject.month, 1 ])
    }


    /**
     * Validate a date as enabled and shift if needed.
     */
    DatePicker.prototype.validate = function( type, dateObject, options ) {

        var calendar = this,

            // Keep a reference to the original date.
            originalDateObject = dateObject,

            // Make sure we have an interval.
            interval = options && options.interval ? options.interval : 1,

            // Check if the calendar enabled dates are inverted.
            isInverted = calendar.item.enable === -1,

            // Check if we have any enabled dates after/before now.
            hasEnabledBeforeTarget, hasEnabledAfterTarget,

            // The min & max limits.
            minLimitObject = calendar.item.min,
            maxLimitObject = calendar.item.max,

            // Check if we’ve reached the limit during shifting.
            reachedMin, reachedMax,

            // Check if the calendar is inverted and at least one weekday is enabled.
            hasEnabledWeekdays = isInverted && calendar.item.disable.filter( function( value ) {

                // If there’s a date, check where it is relative to the target.
                if ( $.isArray( value ) ) {
                    var dateTime = calendar.create( value ).pick
                    if ( dateTime < dateObject.pick ) hasEnabledBeforeTarget = true
                    else if ( dateTime > dateObject.pick ) hasEnabledAfterTarget = true
                }

                // Return only integers for enabled weekdays.
                return Picker._.isInteger( value )
            }).length



        // Cases to validate for:
        // [1] Not inverted and date disabled.
        // [2] Inverted and some dates enabled.
        // [3] Out of range.
        //
        // Cases to **not** validate for:
        // • Navigating months.
        // • Not inverted and date enabled.
        // • Inverted and all dates disabled.
        // • ..and anything else.
        if ( !options.nav ) if (
            /* 1 */ ( !isInverted && calendar.disabled( dateObject ) ) ||
            /* 2 */ ( isInverted && calendar.disabled( dateObject ) && ( hasEnabledWeekdays || hasEnabledBeforeTarget || hasEnabledAfterTarget ) ) ||
            /* 3 */ ( dateObject.pick <= minLimitObject.pick || dateObject.pick >= maxLimitObject.pick )
        ) {


            // When inverted, flip the direction if there aren’t any enabled weekdays
            // and there are no enabled dates in the direction of the interval.
            if ( isInverted && !hasEnabledWeekdays && ( ( !hasEnabledAfterTarget && interval > 0 ) || ( !hasEnabledBeforeTarget && interval < 0 ) ) ) {
                interval *= -1
            }


            // Keep looping until we reach an enabled date.
            while ( calendar.disabled( dateObject ) ) {


                // If we’ve looped into the next/prev month, return to the original date and flatten the interval.
                if ( Math.abs( interval ) > 1 && ( dateObject.month < originalDateObject.month || dateObject.month > originalDateObject.month ) ) {
                    dateObject = originalDateObject
                    interval = Math.abs( interval ) / interval
                }


                // If we’ve reached the min/max limit, reverse the direction and flatten the interval.
                if ( dateObject.pick <= minLimitObject.pick ) {
                    reachedMin = true
                    interval = 1
                }
                else if ( dateObject.pick >= maxLimitObject.pick ) {
                    reachedMax = true
                    interval = -1
                }


                // If we’ve reached both limits, just break out of the loop.
                if ( reachedMin && reachedMax ) {
                    break
                }


                // Finally, create the shifted date using the interval and keep looping.
                dateObject = calendar.create([ dateObject.year, dateObject.month, dateObject.date + interval ])
            }

        } //endif


        // Return the date object settled on.
        return dateObject
    } //DatePicker.prototype.validate


    /**
     * Check if a date is disabled.
     */
    DatePicker.prototype.disabled = function( dateObject ) {

        var calendar = this,

            // Filter through the disabled dates to check if this is one.
            isDisabledDate = !!calendar.item.disable.filter( function( dateToDisable ) {

                // If the date is a number, match the weekday with 0index and `firstDay` check.
                if ( Picker._.isInteger( dateToDisable ) ) {
                    return dateObject.day === ( calendar.settings.firstDay ? dateToDisable : dateToDisable - 1 ) % 7
                }

                // If it’s an array or a native JS date, create and match the exact date.
                if ( $.isArray( dateToDisable ) || Picker._.isDate( dateToDisable ) ) {
                    return dateObject.pick === calendar.create( dateToDisable ).pick
                }
            }).length


        // Check the calendar “enabled” flag and respectively flip the
        // disabled state. Then also check if it’s beyond the min/max limits.
        return calendar.item.enable === -1 ? !isDisabledDate : isDisabledDate ||
            dateObject.pick < calendar.item.min.pick ||
            dateObject.pick > calendar.item.max.pick

    } //DatePicker.prototype.disabled


    /**
     * Parse a string into a usable type.
     */
    DatePicker.prototype.parse = function( type, value, options ) {

        var calendar = this,
            parsingObject = {}

        if ( !value || Picker._.isInteger( value ) || $.isArray( value ) || Picker._.isDate( value ) || Picker._.isObject( value ) && Picker._.isInteger( value.pick ) ) {
            return value
        }

        // We need a `.format` to parse the value.
        if ( !( options && options.format ) ) {
            // should probably default to the default format.
            throw "Need a formatting option to parse this.."
        }

        // Convert the format into an array and then map through it.
        calendar.formats.toArray( options.format ).map( function( label ) {

            var
                // Grab the formatting label.
                formattingLabel = calendar.formats[ label ],

                // The format length is from the formatting label function or the
                // label length without the escaping exclamation (!) mark.
                formatLength = formattingLabel ? Picker._.trigger( formattingLabel, calendar, [ value, parsingObject ] ) : label.replace( /^!/, '' ).length

            // If there's a format label, split the value up to the format length.
            // Then add it to the parsing object with appropriate label.
            if ( formattingLabel ) {
                parsingObject[ label ] = value.substr( 0, formatLength )
            }

            // Update the value as the substring from format length to end.
            value = value.substr( formatLength )
        })

        // If it’s parsing a user provided month value, compensate for month 0index.
        return [ parsingObject.yyyy || parsingObject.yy, +( parsingObject.mm || parsingObject.m ) - ( options.data ?  1 : 0 ), parsingObject.dd || parsingObject.d ]
    } //DatePicker.prototype.parse


    /**
     * Various formats to display the object in.
     */
    DatePicker.prototype.formats = (function() {

        // Return the length of the first word in a collection.
        function getWordLengthFromCollection( string, collection, dateObject ) {

            // Grab the first word from the string.
            var word = string.match( /\w+/ )[ 0 ]

            // If there's no month index, add it to the date object
            if ( !dateObject.mm && !dateObject.m ) {
                dateObject.m = collection.indexOf( word )
            }

            // Return the length of the word.
            return word.length
        }

        // Get the length of the first word in a string.
        function getFirstWordLength( string ) {
            return string.match( /\w+/ )[ 0 ].length
        }

        return {

            d: function( string, dateObject ) {

                // If there's string, then get the digits length.
                // Otherwise return the selected date.
                return string ? Picker._.digits( string ) : dateObject.date
            },
            dd: function( string, dateObject ) {

                // If there's a string, then the length is always 2.
                // Otherwise return the selected date with a leading zero.
                return string ? 2 : Picker._.lead( dateObject.date )
            },
            ddd: function( string, dateObject ) {

                // If there's a string, then get the length of the first word.
                // Otherwise return the short selected weekday.
                return string ? getFirstWordLength( string ) : this.settings.weekdaysShort[ dateObject.day ]
            },
            dddd: function( string, dateObject ) {

                // If there's a string, then get the length of the first word.
                // Otherwise return the full selected weekday.
                return string ? getFirstWordLength( string ) : this.settings.weekdaysFull[ dateObject.day ]
            },
            m: function( string, dateObject ) {

                // If there's a string, then get the length of the digits
                // Otherwise return the selected month with 0index compensation.
                return string ? Picker._.digits( string ) : dateObject.month + 1
            },
            mm: function( string, dateObject ) {

                // If there's a string, then the length is always 2.
                // Otherwise return the selected month with 0index and leading zero.
                return string ? 2 : Picker._.lead( dateObject.month + 1 )
            },
            mmm: function( string, dateObject ) {

                var collection = this.settings.monthsShort

                // If there's a string, get length of the relevant month from the short
                // months collection. Otherwise return the selected month from that collection.
                return string ? getWordLengthFromCollection( string, collection, dateObject ) : collection[ dateObject.month ]
            },
            mmmm: function( string, dateObject ) {

                var collection = this.settings.monthsFull

                // If there's a string, get length of the relevant month from the full
                // months collection. Otherwise return the selected month from that collection.
                return string ? getWordLengthFromCollection( string, collection, dateObject ) : collection[ dateObject.month ]
            },
            yy: function( string, dateObject ) {

                // If there's a string, then the length is always 2.
                // Otherwise return the selected year by slicing out the first 2 digits.
                return string ? 2 : ( '' + dateObject.year ).slice( 2 )
            },
            yyyy: function( string, dateObject ) {

                // If there's a string, then the length is always 4.
                // Otherwise return the selected year.
                return string ? 4 : dateObject.year
            },

            // Create an array by splitting the formatting string passed.
            toArray: function( formatString ) { return formatString.split( /(d{1,4}|m{1,4}|y{4}|yy|!.)/g ) },

            // Format an object into a string using the formatting options.
            toString: function ( formatString, itemObject ) {
                var calendar = this
                return calendar.formats.toArray( formatString ).map( function( label ) {
                    return Picker._.trigger( calendar.formats[ label ], calendar, [ 0, itemObject ] ) || label.replace( /^!/, '' )
                }).join( '' )
            }
        }
    })() //DatePicker.prototype.formats


    /**
     * Flip an item as enabled or disabled.
     */
    DatePicker.prototype.flipItem = function( type, value/*, options*/ ) {

        var calendar = this,
            collection = calendar.item.disable,
            isInverted = calendar.item.enable === -1

        // Flip the enabled and disabled dates.
        if ( value == 'flip' ) {
            calendar.item.enable = isInverted ? 1 : -1
        }

        // Reset the collection and enable the base state.
        else if ( ( type == 'enable' && value === true ) || ( type == 'disable' && value === false ) ) {
            calendar.item.enable = 1
            collection = []
        }

        // Reset the collection and disable the base state.
        else if ( ( type == 'enable' && value === false ) || ( type == 'disable' && value === true ) ) {
            calendar.item.enable = -1
            collection = []
        }

        // Make sure a collection of things was passed to add/remove.
        else if ( $.isArray( value ) ) {

            // Check if we have to add/remove from collection.
            if ( !isInverted && type == 'enable' || isInverted && type == 'disable' ) {
                collection = calendar.removeDisabled( collection, value )
            }
            else if ( !isInverted && type == 'disable' || isInverted && type == 'enable' ) {
                collection = calendar.addDisabled( collection, value )
            }
        }

        return collection
    } //DatePicker.prototype.flipItem


    /**
     * Add an item to the disabled collection.
     */
    DatePicker.prototype.addDisabled = function( collection, item ) {
        var calendar = this
        item.map( function( timeUnit ) {
            if ( !calendar.filterDisabled( collection, timeUnit ).length ) {
                collection.push( timeUnit )
            }
        })
        return collection
    } //DatePicker.prototype.addDisabled


    /**
     * Remove an item from the disabled collection.
     */
    DatePicker.prototype.removeDisabled = function( collection, item ) {
        var calendar = this
        item.map( function( timeUnit ) {
            collection = calendar.filterDisabled( collection, timeUnit, 1 )
        })
        return collection
    } //DatePicker.prototype.removeDisabled


    /**
     * Filter through the disabled collection to find a time unit.
     */
    DatePicker.prototype.filterDisabled = function( collection, timeUnit, isRemoving ) {

        var calendar = this,

            // Check if the time unit passed is an array or date object.
            timeIsObject = $.isArray( timeUnit ) || Picker._.isDate( timeUnit ),

            // Grab the comparison value if it’s an object.
            timeObjectValue = timeIsObject && calendar.create( timeUnit ).pick

        // Go through the disabled collection and try to match this time unit.
        return collection.filter( function( disabledTimeUnit ) {

            // Check if it’s an object and the collection item is an object,
            // use the comparison values. Otherwise to a direct comparison.
            var isMatch = timeIsObject && ( $.isArray( disabledTimeUnit ) || Picker._.isDate( disabledTimeUnit ) ) ?
                    timeObjectValue === calendar.create( disabledTimeUnit ).pick : timeUnit === disabledTimeUnit

            // Invert the match if we’re removing from the collection.
            return isRemoving ? !isMatch : isMatch
        })
    } //DatePicker.prototype.filterDisabled


    /**
     * Create a string for the nodes in the picker.
     */
    DatePicker.prototype.nodes = function( isOpen ) {

        var
            calendar = this,
            settings = calendar.settings,
            nowObject = calendar.item.now,
            selectedObject = calendar.item.select,
            highlightedObject = calendar.item.highlight,
            viewsetObject = calendar.item.view,
            disabledCollection = calendar.item.disable,
            minLimitObject = calendar.item.min,
            maxLimitObject = calendar.item.max,


            // Create the calendar table head using a copy of weekday labels collection.
            // * We do a copy so we don't mutate the original array.
            tableHead = (function( collection ) {

                // If the first day should be Monday, move Sunday to the end.
                if ( settings.firstDay ) {
                    collection.push( collection.shift() )
                }

                // Create and return the table head group.
                return Picker._.node(
                    'thead',
                    Picker._.group({
                        min: 0,
                        max: DAYS_IN_WEEK - 1,
                        i: 1,
                        node: 'th',
                        item: function( counter ) {
                            return [
                                collection[ counter ],
                                settings.klass.weekdays
                            ]
                        }
                    })
                ) //endreturn
            })( ( settings.showWeekdaysFull ? settings.weekdaysFull : settings.weekdaysShort ).slice( 0 ) ), //tableHead


            // Create the nav for next/prev month.
            createMonthNav = function( next ) {

                // Otherwise, return the created month tag.
                return Picker._.node(
                    'div',
                    ' ',
                    settings.klass[ 'nav' + ( next ? 'Next' : 'Prev' ) ] + (

                        // If the focused month is outside the range, disabled the button.
                        ( next && viewsetObject.year >= maxLimitObject.year && viewsetObject.month >= maxLimitObject.month ) ||
                        ( !next && viewsetObject.year <= minLimitObject.year && viewsetObject.month <= minLimitObject.month ) ?
                        ' ' + settings.klass.navDisabled : ''
                    ),
                    'data-nav=' + ( next || -1 )
                ) //endreturn
            }, //createMonthNav


            // Create the month label.
            createMonthLabel = function( monthsCollection ) {

                // If there are months to select, add a dropdown menu.
                if ( settings.selectMonths ) {

                    return Picker._.node( 'select', Picker._.group({
                        min: 0,
                        max: 11,
                        i: 1,
                        node: 'option',
                        item: function( loopedMonth ) {

                            return [

                                // The looped month and no classes.
                                monthsCollection[ loopedMonth ], 0,

                                // Set the value and selected index.
                                'value=' + loopedMonth +
                                ( viewsetObject.month == loopedMonth ? ' selected' : '' ) +
                                (
                                    (
                                        ( viewsetObject.year == minLimitObject.year && loopedMonth < minLimitObject.month ) ||
                                        ( viewsetObject.year == maxLimitObject.year && loopedMonth > maxLimitObject.month )
                                    ) ?
                                    ' disabled' : ''
                                )
                            ]
                        }
                    }), settings.klass.selectMonth, isOpen ? '' : 'disabled' )
                }

                // If there's a need for a month selector
                return Picker._.node( 'div', monthsCollection[ viewsetObject.month ], settings.klass.month )
            }, //createMonthLabel


            // Create the year label.
            createYearLabel = function() {

                var focusedYear = viewsetObject.year,

                // If years selector is set to a literal "true", set it to 5. Otherwise
                // divide in half to get half before and half after focused year.
                numberYears = settings.selectYears === true ? 5 : ~~( settings.selectYears / 2 )

                // If there are years to select, add a dropdown menu.
                if ( numberYears ) {

                    var
                        minYear = minLimitObject.year,
                        maxYear = maxLimitObject.year,
                        lowestYear = focusedYear - numberYears,
                        highestYear = focusedYear + numberYears

                    // If the min year is greater than the lowest year, increase the highest year
                    // by the difference and set the lowest year to the min year.
                    if ( minYear > lowestYear ) {
                        highestYear += minYear - lowestYear
                        lowestYear = minYear
                    }

                    // If the max year is less than the highest year, decrease the lowest year
                    // by the lower of the two: available and needed years. Then set the
                    // highest year to the max year.
                    if ( maxYear < highestYear ) {

                        var availableYears = lowestYear - minYear,
                            neededYears = highestYear - maxYear

                        lowestYear -= availableYears > neededYears ? neededYears : availableYears
                        highestYear = maxYear
                    }

                    return Picker._.node( 'select', Picker._.group({
                        min: lowestYear,
                        max: highestYear,
                        i: 1,
                        node: 'option',
                        item: function( loopedYear ) {
                            return [

                                // The looped year and no classes.
                                loopedYear, 0,

                                // Set the value and selected index.
                                'value=' + loopedYear + ( focusedYear == loopedYear ? ' selected' : '' )
                            ]
                        }
                    }), settings.klass.selectYear, isOpen ? '' : 'disabled' )
                }

                // Otherwise just return the year focused
                return Picker._.node( 'div', focusedYear, settings.klass.year )
            } //createYearLabel


        // Create and return the entire calendar.
        return Picker._.node(
            'div',
            createMonthNav() + createMonthNav( 1 ) +
            createMonthLabel( settings.showMonthsShort ? settings.monthsShort : settings.monthsFull ) +
            createYearLabel(),
            settings.klass.header
        ) + Picker._.node(
            'table',
            tableHead +
            Picker._.node(
                'tbody',
                Picker._.group({
                    min: 0,
                    max: WEEKS_IN_CALENDAR - 1,
                    i: 1,
                    node: 'tr',
                    item: function( rowCounter ) {

                        // If Monday is the first day and the month starts on Sunday, shift the date back a week.
                        var shiftDateBy = settings.firstDay && calendar.create([ viewsetObject.year, viewsetObject.month, 1 ]).day === 0 ? -7 : 0

                        return [
                            Picker._.group({
                                min: DAYS_IN_WEEK * rowCounter - viewsetObject.day + shiftDateBy + 1, // Add 1 for weekday 0index
                                max: function() {
                                    return this.min + DAYS_IN_WEEK - 1
                                },
                                i: 1,
                                node: 'td',
                                item: function( targetDate ) {

                                    // Convert the time date from a relative date to a target date.
                                    targetDate = calendar.create([ viewsetObject.year, viewsetObject.month, targetDate + ( settings.firstDay ? 1 : 0 ) ])

                                    return [
                                        Picker._.node(
                                            'div',
                                            targetDate.date,
                                            (function( klasses ) {

                                                // Add the `infocus` or `outfocus` classes based on month in view.
                                                klasses.push( viewsetObject.month == targetDate.month ? settings.klass.infocus : settings.klass.outfocus )

                                                // Add the `today` class if needed.
                                                if ( nowObject.pick == targetDate.pick ) {
                                                    klasses.push( settings.klass.now )
                                                }

                                                // Add the `selected` class if something's selected and the time matches.
                                                if ( selectedObject && selectedObject.pick == targetDate.pick ) {
                                                    klasses.push( settings.klass.selected )
                                                }

                                                // Add the `highlighted` class if something's highlighted and the time matches.
                                                if ( highlightedObject && highlightedObject.pick == targetDate.pick ) {
                                                    klasses.push( settings.klass.highlighted )
                                                }

                                                // Add the `disabled` class if something's disabled and the object matches.
                                                if ( disabledCollection && calendar.disabled( targetDate ) || targetDate.pick < minLimitObject.pick || targetDate.pick > maxLimitObject.pick ) {
                                                    klasses.push( settings.klass.disabled )
                                                }

                                                return klasses.join( ' ' )
                                            })([ settings.klass.day ]),
                                            'data-pick=' + targetDate.pick
                                        )
                                    ] //endreturn
                                }
                            })
                        ] //endreturn
                    }
                })
            ),
            settings.klass.table
        ) +

        // * For Firefox forms to submit, make sure to set the buttons’ `type` attributes as “button”.
        Picker._.node(
            'div',
            Picker._.node( 'button', settings.today, settings.klass.buttonToday, 'type=button data-pick=' + nowObject.pick + ( isOpen ? '' : ' disabled' ) ) +
            Picker._.node( 'button', settings.clear, settings.klass.buttonClear, 'type=button data-clear=1' + ( isOpen ? '' : ' disabled' ) ),
            settings.klass.footer
        ) //endreturn
    } //DatePicker.prototype.nodes




    /**
     * The date picker defaults.
     */
    DatePicker.defaults = (function( prefix ) {

        return {

            // Months and weekdays
            monthsFull: [ 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro' ],
            monthsShort: [ 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez' ],
            weekdaysFull: [ 'domingo', 'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado' ],
            weekdaysShort: [ 'dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab' ],

            // Today and clear
            today: 'Hoje',
            clear: 'Limpar',

            // The format to show on the `input` element
            format: 'dd-mm-yyyy',

            // Classes
            klass: {

                table: prefix + 'table',

                header: prefix + 'header',

                navPrev: prefix + 'nav--prev',
                navNext: prefix + 'nav--next',
                navDisabled: prefix + 'nav--disabled',

                month: prefix + 'month',
                year: prefix + 'year',

                selectMonth: prefix + 'select--month',
                selectYear: prefix + 'select--year',

                weekdays: prefix + 'weekday',

                day: prefix + 'day',
                disabled: prefix + 'day--disabled',
                selected: prefix + 'day--selected',
                highlighted: prefix + 'day--highlighted',
                now: prefix + 'day--today',
                infocus: prefix + 'day--infocus',
                outfocus: prefix + 'day--outfocus',

                footer: prefix + 'footer',

                buttonClear: prefix + 'button--clear',
                buttonToday: prefix + 'button--today'
            }
        }
    })( Picker.klasses().picker + '__' )





    /**
     * Extend the picker to add the date picker.
     */
    Picker.extend( 'pickadate', DatePicker )


    }));


/* Proximity event for jQuery
 * ---
 * @author James Padolsey (http://james.padolsey.com)
 * @version 0.1
 * @updated 28-JUL-09
 * ---
 * @info http://github.com/jamespadolsey/jQuery-plugins/proximity-event/
 */

  (function($){
      
      var elems = $([]),
          doc = $(document);
      
      $.event.special.proximity = {
          
          defaults: {
              max: 100,
              min: 0,
              throttle: 0,
              fireOutOfBounds: 1
          },
          
          setup: function(data) {
              
              if (!elems[0])
                  doc.mousemove(handle);
              
              elems = elems.add(this);
              
          },
          
          add: function(o) {
              
              var handler = o.handler,
                  data = $.extend({}, $.event.special.proximity.defaults, o.data),
                  lastCall = 0,
                  nFiredOutOfBounds = 0,
                  hoc = $(this);
              
              o.handler = function(e, pageX, pageY) {
                  
                  var max = data.max,
                      min = data.min,
                      throttle = data.throttle,
                      date = +new Date,
                      distance,
                      proximity,
                      inBounds,
                      fireOutOfBounds = data.fireOutOfBounds;
                  
                  if (throttle && lastCall + throttle > date) {
                      return;
                  }
                  
                  lastCall = date;
                  
                  distance = calcDistance(hoc, pageX, pageY);
                  inBounds = distance < max && distance > min;
                  
                  if (fireOutOfBounds || inBounds) {
                      
                      if (inBounds) {
                          nFiredOutOfBounds = 0;
                      } else {
                          
                          // If fireOutOfBounds is a number then keep incrementing a
                          // counter to determine how many times the handler's been
                          // called out of bounds. Note: the counter is reset whenever
                          // the cursor goes back inBounds...
                          
                          if (typeof fireOutOfBounds === 'number' && nFiredOutOfBounds > fireOutOfBounds) {
                              return;
                          }
                          ++nFiredOutOfBounds;
                      }
                  
                      proximity = e.proximity = 1 - (
                          distance < max ? distance < min ? 0 : distance / max : 1
                      );
                      
                      e.distance = distance;
                      e.pageX = pageX;
                      e.pageY = pageY;
                      e.data = data;
                      
                      return handler.call(this, e, proximity, distance);
                  
                  }
                  
              };
              
          },
          
          teardown: function(){
              
              elems = elems.not(this);
              
              if (!elems[0])
                  doc.unbind('mousemove', handle);
              
          }
          
      };
      
      function calcDistance(el, x, y) {
          
          // Calculate the distance from the closest edge of the element
          // to the cursor's current position
          
          var left, right, top, bottom, offset,
              cX, cY, dX, dY,
              distance = 0;
          
          offset = el.offset();
          left = offset.left;
          top = offset.top;
          right = left + el.outerWidth();
          bottom = top + el.outerHeight();
          
          cX = x > right ? right : x > left ? x : left;
          cY = y > bottom ? bottom : y > top ? y : top;
          
          dX = Math.abs( cX - x );
          dY = Math.abs( cY - y );
          
          return Math.sqrt( dX * dX + dY * dY );
              
      }
      
      function handle(e) {
          
          var x = e.pageX,
              y = e.pageY,
              i = -1,
              fly = $([]);
          
          while (fly[0] = elems[++i]) {
              fly.triggerHandler('proximity', [x,y]);
          }
          
      }
      
  }(jQuery));