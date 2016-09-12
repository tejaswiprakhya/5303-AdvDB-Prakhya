Tejaswi Prakhya
104.131.64.127
http://104.131.64.127/phpmyadmin
gift_options.sql
CREATE TABLE IF NOT EXISTS `gift_options` (
        `allowGiftWrap` BOOLEAN NOT NULL,
        `allowGiftMessage` BOOLEAN NOT NULL,
        `allowGiftReceipt` BOOLEAN NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
image_entities.sql
CREATE TABLE IF NOT EXISTS `image_entities` (
        `thumbnailImage` tinyblob NOT NULL,
        `mediumImage` mediumbolb NOT NULL,
        `largeImage` longblob NOT NULL,
        `entityType` varchar ( 9 ) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE `image_entities`
   ADD PRIMARY KEY(
     `entityType`);
market_place_price.sql
CREATE TABLE IF NOT EXISTS `market_place_price` (
        `price` double NOT NULL,
        `sellerInfo` varchar ( 44 ) NOT NULL,
        `standardShipRate` double NOT NULL,
        `twoThreeDayShippingRate` double NOT NULL,
        `availableOnline` boolean NOT NULL,
        `clearance` boolean NOT NULL,
        `offerType` varchar ( 16 ) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE `market_place_price`
   ADD PRIMARY KEY(
     `price`);
products.sql
CREATE TABLE IF NOT EXISTS `products` (
        `itemId` INT( 9 ) NOT NULL,
        `parentItemId` INT( 9 ) NOT NULL,
        `name` varchar( 200 ) NOT NULL,
        `salePrice` DOUBLE NOT NULL,
        `upc` varchar( 12 ) NOT NULL,
        `categoryPath` varchar ( 123 ) NOT NULL,
        `shortDescription` TEXT ( 1112 ) NOT NULL,
        `longDescription` TEXT ( 5540 ) NOT NULL,
        `brandName` varchar ( 36 ) NOT NULL,
        `thumbnailImage` varchar ( 149 ) NOT NULL,
        `mediumImage` varchar ( 149 ) NOT NULL,
        `largeImage` varchar ( 149 ) NOT NULL,
        `productTrackingUrl` varchar ( 416 ) NOT NULL,
        `modelNumber` varchar ( 53 ) NOT NULL,
        `productUrl` varchar ( 345 ) NOT NULL,
        `categoryNode` varchar ( 23 )NOT NULL,
        `stock` varchar ( 13 ) NOT NULL,
        `addToCartUrl` varchar ( 221 ) NOT NULL,
        `affiliateAddToCartUrl`varchar ( 296 ) NOT NULL,
        `offerType` varchar ( 16 ) NOT NULL,
        `msrp` DOUBLE NOT NULL,
        `standardShipRate` DOUBLE NOT NULL,
        `color` varchar ( 10 )  NOT NULL,
        `customerRating` varchar ( 5 ) NOT NULL,
        `numReviews` INT ( 5 ) NOT NULL,
        `customerRatingImage` varchar ( 48 ) NOT NULL,
        `maxItemsInOrder` INT ( 6 ) NOT NULL,
        `size` varchar ( 49 ) NOT NULL,
        `sellerInfo` varchar ( 49 ) NOT NULL,
        `age` varchar ( 14 ) NOT NULL,
        `gender` varchar ( 6 ) NOT NULL,
        `isbn` varchar ( 13 ) NOT NULL,
        `preOrderShipsOn` varchar ( 19 ) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE `products`
   ADD PRIMARY KEY(
     `itemId`,
     `parentItemId`);
