// document.querySelector("#root > div > div > div > div:nth-child(7) > div.top-left--jiLTk > div > div > div > div.header--3V5d-").textContent = "Count"
TotalCount = 0;
CardsOnTable = [];

countCards = function (cards) {
    count = 0;
    for (const card of cards) {
        if ("AKQJT".includes(card[0])) {
            count -= 1;
        }
        else if ("23456".includes(card[0])) {
            count += 1;
        }
    }
    return count;
}

pulse = function (arg) {
    if (arg[0].hasOwnProperty("payloadData")) {
        payload = arg[0].payloadData;
    }
    else {
        return;
    }

    if (payload.hasOwnProperty("name")) {
        if (payload.name == "BetweenGames") {
            TotalCount += countCards(CardsOnTable);
            CardsOnTable = [];
        }
    }
    else if (payload.hasOwnProperty("dealer")) {
        CardsOnTable = [];

        // Dealer
        for (const card of payload.dealer.cards) {
            if (card.value != "**") {
                CardsOnTable.push(card.value)
            }
        }

        // Players
        for (const [k, player] of Object.entries(payloadData.seats)) {
            for (const card of player.first.cards) {
                CardsOnTable.push(card.value)
            }
        }

        console.stdlog(console, ["TotalCount:", TotalCount + countCards(CardsOnTable)])
    }
}

console.stdlog = console.log.bind(console);
console.logs = [];
console.log = function () {
    console.logs.push(Array.from(arguments));
    console.stdlog.apply(console, arguments);
    pulse(Array.from(arguments));
}

