// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }
    return items
}

// you receive an array of objects which you must filter by all its keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {

    // for (let i=0; i<items.length; i++) {
    //     let item = items[i];
    //     let object = Object.values(item).filter((item) => item.includes(filterValue) )
    //     console.log(object)
    // }

    for (let i=0; i<items.length; i++) {
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
    let body = document.body;
    body.classList.toggle("dark-mode");
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

function increaseFont(id, increaseFactor) {
    let txt = document.getElementById(id);
    let style = window.getComputedStyle(txt, null).getPropertyValue('font-size');
    let currentSize = parseFloat(style);
    txt.style.fontSize = (currentSize + increaseFactor) + 'px';
    console.log("increaseFont");
}

function decreaseFont(id, decreaseFactor) {
    let txt = document.getElementById(id);
    let style = window.getComputedStyle(txt, null).getPropertyValue('font-size');
    let currentSize = parseFloat(style);
    txt.style.fontSize = (currentSize + decreaseFactor) + 'px';
    console.log("decreaseFont")
}