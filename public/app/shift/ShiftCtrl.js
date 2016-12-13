(function(){
    function ShiftCtrl($scope, SessionService, ShiftService, $ionicPopup, $rootScope) {
        $scope.logout = logout;

        $rootScope.$on("session:loggedIn", function(user){
            initialize();
        });

        function initialize() {
            // mock begin shift
            ShiftService.openShift(
                SessionService.currentUser(),
                0
            ).then(function(shift){
                $scope.shift = shift;
            }, function(error) {
                $ionicPopup.alert({
                    title: "Error",
                    template: error
                });
                SessionService.logout();
            });
        }

        function logout() {
            var balance = ShiftService.getShift().currentBalance;
            ShiftService.closeShift(balance).then(function() {
                SessionService.logout();
            }, function(error) {
                $ionicPopup.alert({
                    title: "Error",
                    template: error,
                });
            });
        }

        initialize();
    }

    angular.module('pulltabs.pos').controller('ShiftCtrl', ['$scope', 'SessionService', 'ShiftService', '$ionicPopup', '$rootScope', ShiftCtrl]);
})();
