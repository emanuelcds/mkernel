(function(){
    'use strict';

    function MainCtrl($scope, $rootScope, PinService, SessionService) {

        function initialize() {
            // if not logged in, force login
            SessionService.assureLogged();
            PinService.getPins().then(function(data){
                console.log(data);
                $rootScope.pinCount = data.filter(function(e){return e.status == 'new'}).length;
                $rootScope.cashOutRequestCount = data.filter(function(e){return e.status == 'cashout'}).length;
            });
        }

        function onLogout() {
            SessionService.logout();
            if($rootScope.shift) {
                delete $rootScope.shift;
            }
        }

        initialize();
    }

    angular.module('pulltabs.pos').controller('MainCtrl', ['$scope', '$rootScope', 'PinService', 'SessionService', MainCtrl]);
})();
