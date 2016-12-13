(function(){
    'use strict';

    function CashoutCtrl($scope, $rootScope, PinService, $ionicPopup, $interval) {
        $scope.cashout      = cashoutPin;
        $scope.updatePins   = updatePins;

        function cashoutPin(number) {
            PinService.getPin(number).then(function(pin) {
                if(pin.status != 'cashout') {
                    $ionicPopup.alert({
                        title: "Error",
                        template:"This PIN didn't requested cashout."
                    });

                    return false;
                }

                $ionicPopup.confirm({
                    title: 'Pin Cashout',
                    template: 'Withdraw "'+number+'"?'
                }).then(function(confirm){
                    if(confirm) {
                        PinService.cashOutPin(number).then(
                        function(){
                            $ionicPopup.alert({
                                title: 'Cashout PIN',
                                template: 'Cashout successfully!'
                            });
                            updatePins();
                        }, function(msg){
                            $ionicPopup.alert({
                                title: 'Cashout PIN',
                                template: msg
                            });
                        });
                    }
                }); // end popup confirm
            }); // end pin service get pin
       }

        function updatePins() {
            PinService.getPins().then(
                function(data) {
                    if(data && data.length) {
                        $scope.cashOutPins = data.filter(function(e){
                            return e.status == "cashout";
                        });
                        console.log("Pins from Cashout: ", $scope.cashOutPins);
                        $rootScope.cashOutRequestCount = $scope.cashOutPins.length;
                    }
                },
                function() {
                    $scope.cashOutPins = null;
                    console.log("Could not gather cashout pins!");
                }
            );
        }

        function startWatcher() {
            if(!$scope.cashoutWatcher) {
                $scope.cashoutWatcher = $interval(updatePins, 30000);
            }
            updatePins();
        }

        function stopWatcher() {
            $interval.cancel($scope.cashoutWatcher);
            delete $scope.cashoutWatcher;
        }

        function initialize() {
            startWatcher();
            $rootScope.$on("session:loggedIn", startWatcher);
            $rootScope.$on("session:loggedOut", stopWatcher);
            $rootScope.$on("pin:forcedCashout", updatePins);
        }

        initialize();

    }

    angular.module('pulltabs.pos').controller('CashoutCtrl', ['$scope', '$rootScope', 'PinService', '$ionicPopup', '$interval', CashoutCtrl]);
})();
