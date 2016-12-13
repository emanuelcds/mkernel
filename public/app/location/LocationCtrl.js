(function(module){
    'use strict';

    function LocationCtrl($rootScope, $state, SessionService) {
        var page = this;

        page.logout = logout;
        page.confirmLocation = confirmLocation;

        function logout() {
            SessionService.logout();
        }

        function confirmLocation() {
            if(page.selectedLocation) {
                SessionService.setLocation(page.selectedLocation);
                $state.go('app.shift');
            }
        }

        function initialize() {
            SessionService.assureLogged();
            if(SessionService.currentUser()) {
                page.locations = SessionService.currentUser().locations;
            }

            page.selectedLocation = null;
        }

        initialize();
        $rootScope.$on("session:loggedIn", initialize);
    }



    module.controller('LocationCtrl', LocationCtrl);
})(angular.module('pulltabs.pos'))
