(function(){

'use strict';

angular.module('pulltabs.pos', [
    'ionic', 
    'ng-currency', 
    'angularMoment',
    'ui.gravatar'
])

// Routes
.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/login');

    $stateProvider

    // login state
    .state('login', {
        url: '/login',
        templateUrl: 'app/login/index.html',
        controller: 'LoginCtrl as page'
    })

    // select location state
    .state('location', {
        url: '/location',
        templateUrl: 'app/location/index.html',
        controller: 'LocationCtrl as page'
    })

    // app pre-guard state (can only enter on app after logging in)
    .state('app', {
        templateUrl: 'app/main/tabs.html',
        abstract: true,
        controller: 'MainCtrl'
    })

    // app shift tab
    .state('app.shift', {
        url: '/shift',
        views: {
            'tab-shift': {
                templateUrl: 'app/shift/index.html',
                controller: 'ShiftCtrl'
            }
        }
    })

    // app pin tab
    .state('app.pin', {
        url: '/pins',
        views: {
            'tab-pins': {
                templateUrl: 'app/pin/index.html',
                controller: 'PinCtrl'
            }
        }
    })

    // app cashout tab
    .state('app.cashout', {
        url: '/cashout',
        views: {
            'tab-cashout': {
                templateUrl: 'app/cashout/index.html',
                controller: 'CashoutCtrl'
            }
        }
    });
})

// Ionic Config
.config(function($ionicConfigProvider) {
    $ionicConfigProvider.tabs.position('bottom');
})

// Startup and Bootstrap
.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if(window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
})

})();
