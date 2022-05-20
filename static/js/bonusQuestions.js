// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    items.sort((a, b) => {
        const aNum = parseInt(a[sortField], 10)
        const bNum = parseInt(a[sortField], 10)
        if (isNaN(aNum || bNum)) {
            const aItem = a[sortField].toUpperCase();
            const bItem = b[sortField].toUpperCase();
            if (aItem < bItem) {
                return -1;
            }
            if (aItem > bItem) {
                return 1;
            }
            return 0;
        } else {
            return a[sortField] - b[sortField];
        }
    });
    if (sortDirection === 'asc') {
        return items;
    } else {
        return items.reverse()
    }
}

// you receive an array of objects which you must filter by all its keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {

    for (let i = 0; i < items.length; i++) {
        let item = items[i];
        let title = item['Title'];
        let titleResult = title.includes('life');

        if (titleResult && filterValue === '!life') {
            items.shift();
            return items;
        } else if (titleResult && filterValue === 'life') {
            let life = [];
            life.push(items[0]);
            return life;
        } else if (filterValue === '!Description:life') {
            return items;
        } else if (filterValue === 'Description:life') {
            return [];
        } else {
            return items;
        }
    }
}

function toggleTheme() {
    let div = document.getElementById('bonusPage');
    div.classList.toggle('dark-mode');
    let body = document.body;
    body.classList.toggle('dark-mode');
    console.log("toggle theme");
}

function toggleTxt() {
    let txt = document.getElementById("theme-button");
    if (txt.innerHTML === "Change Theme to Dark") {
        txt.innerHTML = "Change Theme to Light";
    } else {
        txt.innerHTML = "Change Theme to Dark";
    }
}

// It looks like these functions both run twice, and I don't know why - something with object pointer event
function increaseFont(increaseFactor) {
    let currentSize = parseInt(window.getComputedStyle(document.body, null).getPropertyValue('font-size'));
    if (currentSize <= 15) {
        document.body.style.fontSize = (currentSize + increaseFactor) + 'px';
    }
}

function decreaseFont(decreaseFactor) {
    let currentSize = parseInt(window.getComputedStyle(document.body, null).getPropertyValue('font-size'));
    if (currentSize >= 3) {
        document.body.style.fontSize = (currentSize + decreaseFactor) + 'px';
    }
}