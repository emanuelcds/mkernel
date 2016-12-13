(function(){
    'use strict';

    function LoginCtrl($rootScope, $state, $ionicPopup,  SessionService) {
        var page = this;

        page.user = {
            email: "",
            password: ""
        };
        page.login = login;

        function login() {
            SessionService.login(page.user.email, page.user.password).then(
            function(user) {
                page.user = user;
            }, function(error) {
                $ionicPopup.alert({
                    title: 'Error',
                    template: error
                });
            });
            clearFields();
        }

        function initialize() {
            clearFields();
            if($rootScope.shift) {
                delete $rootScope.shift;
            }
        }

        function clearFields() {
            page.user = {
                email: "",
                password: ""
            };
        }

        initialize();
    }

    angular.module('pulltabs.pos').controller('LoginCtrl', LoginCtrl);
})();
