// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Rental {
    struct Location {
        int256 lat;
        int256 lon;
    }

    struct Product {
        uint256 pid;
        string name;
        uint256 priceInWei;
        bool available;
        address owner;
        address renter;
        uint256 rentalStartTime;
        uint256 rentalDuration;
        uint256 radius;
        bool subRentAllowed;
        address subRentRequester;
        uint256 commissionRate;
    }

    uint256 public nextProductId;
    mapping(uint256 => Product) public products;
    mapping(uint256 => Location) public productLocations;
    mapping(address => bool) public bannedUsers;

    event ProductAdded(uint256 pid, string name, uint256 priceInWei, address owner, uint256 radius);
    event ProductRented(uint256 pid, address renter, uint256 rentalDuration, int256 lat, int256 lon);
    event ProductSubRented(uint256 pid, address subRenter, uint256 rentalDuration, uint256 commission, int256 lat, int256 lon);
    event ProductReturned(uint256 pid, bool penalized, int256 lat, int256 lon);
    event UserBanned(address bannedUser, uint256 pid);
    event LocationUpdated(uint256 pid, int256 lat, int256 lon);

    function addProduct(
        string memory _name,
        uint256 _priceInWei,
        int256 _lat,
        int256 _lon,
        uint256 _radius,
        bool _subAllowed
    ) public {
        uint256 pid = nextProductId;
        products[pid] = Product({
            pid: pid,
            name: _name,
            priceInWei: _priceInWei,
            available: true,
            owner: msg.sender,
            renter: address(0),
            rentalStartTime: 0,
            rentalDuration: 0,
            radius: _radius,
            subRentAllowed: _subAllowed,
            subRentRequester: address(0),
            commissionRate: 5
        });

        productLocations[pid] = Location(_lat, _lon);

        emit ProductAdded(pid, _name, _priceInWei, msg.sender, _radius);
        nextProductId++;
    }

    function rentProduct(uint256 _pid, uint256 _rentalDuration, int256 _lat, int256 _lon) public payable {
        Product storage p = products[_pid];
        require(!bannedUsers[msg.sender], "Banned from renting");
        require(p.available, "Not available");
        require(p.owner != msg.sender, "Owner cannot rent");
        require(isWithinRadius(_pid, _lat, _lon), "Outside rental radius");
        uint256 totalRent = p.priceInWei * _rentalDuration;
        require(msg.value >= totalRent, "Insufficient ETH");
        p.available = false;
        p.renter = msg.sender;
        p.rentalStartTime = block.timestamp;
        p.rentalDuration = _rentalDuration;

        productLocations[_pid] = Location(_lat, _lon);
        emit LocationUpdated(_pid, _lat, _lon);
        
        uint256 ownerShare = (totalRent * 95) / 100;  // 95% to owner
        uint256 subRenterShare = (totalRent * 5) / 100;
        uint256 remainder = totalRent - (ownerShare + subRenterShare);
        ownerShare += remainder;   
        if(p.subRentRequester == address(0)){
        _transferETH(p.owner, msg.value);
        }
        else{
            _transferETH(p.owner, ownerShare);
            _transferETH(p.subRentRequester, subRenterShare);
        }
        emit ProductRented(_pid, msg.sender, _rentalDuration, _lat, _lon);
    }

    function subRentRequest(uint256 _pid) public {
        Product storage p = products[_pid];
        require(p.subRentAllowed, "Sub-rent not allowed");
        require(p.renter == msg.sender, "Not your rental");
        require(p.subRentRequester == address(0), "Sub-rent already requested");
        p.subRentRequester = msg.sender;
    }

    function approveSubRent(uint256 _pid) public payable {
        Product storage p = products[_pid];
        require(p.owner == msg.sender, "Only owner can approve");
        require(p.subRentAllowed, "Sub-rent not allowed");
        require(p.subRentRequester != address(0), "No sub-rent request");
        p.available = true;
    }

    function returnProduct(uint256 _pid, int256 _lat, int256 _lon) public payable {
        Product storage p = products[_pid];
        require(p.renter == msg.sender, "Not the renter");

        uint256 dueTime = p.rentalStartTime + (p.rentalDuration * 1 hours);
        uint256 currentTime = block.timestamp;
        bool penalized = false;

        if (currentTime > dueTime) {
            uint256 penaltyFee = ((currentTime - dueTime) / 3600) * (p.priceInWei / 2);
            require(msg.value >= penaltyFee, "Penalty required");
            _transferETH(p.owner, penaltyFee);
            penalized = true;
        }

        p.available = true;
        p.renter = address(0);
        p.rentalStartTime = 0;
        p.rentalDuration = 0;

        productLocations[_pid] = Location(_lat, _lon);
        emit LocationUpdated(_pid, _lat, _lon);

        emit ProductReturned(_pid, penalized, _lat, _lon);
    }

    function isWithinRadius(uint256 _pid, int256 lat, int256 lon) public view returns (bool) {
        Location storage loc = productLocations[_pid];
        return approximateDistance(loc.lat, loc.lon, lat, lon) <= products[_pid].radius;
    }

    function approximateDistance(
        int256 lat1,
        int256 lon1,
        int256 lat2,
        int256 lon2
    ) public pure returns (uint256) {
        int256 dLat = lat2 - lat1;
        int256 dLon = lon2 - lon1;
        return uint256(abs(dLat) + abs(dLon));
    }

    function abs(int256 x) internal pure returns (int256) {
        return x < 0 ? -x : x;
    }

    function updateLocation(uint256 _pid, int256 _lat, int256 _lon) public {
        Product storage p = products[_pid];
        require(p.owner == msg.sender, "Only owner can change location");
        productLocations[_pid] = Location(_lat, _lon);

        emit LocationUpdated(_pid, _lat, _lon);
    }

    function _transferETH(address recipient, uint256 amount) private {
        (bool sent, ) = payable(recipient).call{value: amount}("");
        require(sent, "ETH transfer failed");
    }
    function ReportUser(uint256 _pid) public {
        Product storage p = products[_pid];
        
        require(msg.sender == p.owner, "Only owner can ban users");
        require(!p.available, "Product is not rented");
        require(block.timestamp > p.rentalStartTime + p.rentalDuration, "Rental period not over");
        
        bannedUsers[p.renter] = true;  // Ban the renter
        p.available = true;  // Mark product as available again
        p.renter = address(0);  // Clear renter info
        p.rentalStartTime = 0;
        p.rentalDuration = 0;
    
        emit UserBanned(p.renter, _pid);
    }

}
