(function(module){
    'use strict';

    function ShiftService($q, $rootScope) {

        function cashIn(amount) {
            var deferred = $q.defer();

            if(!$rootScope.shift) {
                deferred.reject("Could not cash in without a running shift!");
                return deferred.promise;
            }

            var cashedIn = $rootScope.shift.cashedIn;

            $rootScope.shift.cashedIn = cashedIn + amount || amount;
            $rootScope.shift.currentBalance += amount;
            deferred.resolve($rootScope.shift.cashedIn);

            return deferred.promise;
        }

        function cashOut(amount) {
            var deferred = $q.defer();

            if(!$rootScope.shift) {
                deferred.reject("Could not cash out without a running shift!");
                return deferred.promise;
            }

            var cashedOut = $rootScope.shift.cashedOut;

            $rootScope.shift.cashedOut = cashedOut + amount || amount;
            $rootScope.shift.currentBalance -= amount;
            deferred.resolve($rootScope.shift.cashedOut);

            return deferred.promise;
        }

        function openShift(user, amount) {
            var deferred = $q.defer();

            if($rootScope.shift) {
                deferred.reject("Cannot start a shift with others in progress!");
                return deferred.promise;
            }

            $rootScope.shift = {
                user: user,
                cashedIn: 0,
                cashedOut: 0,
                startedBalance: amount,
                currentBalance: amount,
                startedAt: new Date()
            }

            deferred.resolve($rootScope.shift);

            return deferred.promise;
        }

        function closeShift(balance) {
            var deferred = $q.defer();

            if(!$rootScope.shift) {
                deferred.reject("Cannot close unexistent shift!");
                return deferred.promise;
            }

            delete $rootScope.shift;

            deferred.resolve();

            return deferred.promise;

        }

        function getShift() {
            return $rootScope.shift || null;
        }

        return {
            openShift: openShift,
            closeShift: closeShift,
            cashIn: cashIn,
            cashOut: cashOut,
            getShift: getShift
        }
    }

    module.factory('ShiftService', ['$q', '$rootScope', ShiftService]);
})(angular.module('pulltabs.pos'));
