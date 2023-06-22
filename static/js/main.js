let openDropdown = null;

function outsideClickHandler(event) {
  const target = event.target;
  const dropdown = openDropdown;

  if (dropdown && !dropdown.contains(target)) {
    dropdown.style.display = "none";
    openDropdown = null;
    document.removeEventListener("click", outsideClickHandler);
  }
}

function untilDropdown(btn) {
  const dropdown = btn.nextElementSibling;

  if (openDropdown && openDropdown !== dropdown) {
    openDropdown.style.display = "none";
  }

  const computedStyle = window.getComputedStyle(dropdown);

  if (computedStyle.display === "none") {
    dropdown.style.display = "block";
    openDropdown = dropdown;

    // Remove the event listener before adding it again to ensure
    // only one event listener is active at a time
    document.removeEventListener("click", outsideClickHandler);
    setTimeout(() => {
      document.addEventListener("click", outsideClickHandler);
    }, 0);
  } else {
    dropdown.style.display = "none";
    openDropdown = null;
    document.removeEventListener("click", outsideClickHandler);
  }
}

// Close the dropdown if user clicks outside of any dropdown
document.addEventListener("click", outsideClickHandler);

// function outsideClickHandler(event) {
//   const dropdowns = document.getElementsByClassName("todo-until");
//   const target = event.target;

//   if (!target.closest(".until-div")) {
//     for (let i = 0; i < dropdowns.length; i++) {
//       dropdowns[i].style.display = "none";
//     }
//     document.removeEventListener("click", outsideClickHandler);
//   }
// }

// Datetime
const currentDate = new Date();
const year = currentDate.getFullYear();
const month = String(currentDate.getMonth() + 1).padStart(2, "0");
const day = String(currentDate.getDate()).padStart(2, "0");
const hours = String(currentDate.getHours()).padStart(2, "0");
const minutes = String(currentDate.getMinutes()).padStart(2, "0");
const formattedDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;

var dtLoc = document.getElementById("dtLoc");
dtLoc.value = formattedDateTime;
dtLoc.min = formattedDateTime;

try {
  var input1 = document.getElementById("filterInput");
  var input2 = document.getElementById("filterInputMob");
  var inputH = document.getElementById("foldersHidden");
  var sharedValue = "";

  // Event listener for input 1
  input1.addEventListener("input", function () {
    sharedValue = input1.value;
    input2.value = sharedValue;
    inputH.value = sharedValue;
    // console.log("Shared value updated to:", inputH.value);
  });

  // Event listener for input 2
  input2.addEventListener("input", function () {
    sharedValue = input2.value;
    input1.value = sharedValue;
    inputH.value = sharedValue;
    // console.log("Shared value updated to:", inputH.value);
  });
} catch {}

if (document.getElementById("foldersHidden")) {
  console.log("init");
  // const filterInput = document.getElementById("filterInput");
  const divContainer = document.getElementById("divContainer");
  const filterItems = divContainer.getElementsByClassName("filterItem");
  const divContainerMob = document.getElementById("divContainerMob");
  const filterItemsMob = divContainerMob.getElementsByClassName("filterItem");
  function handleFilterItems() {
    console.log(inputH);
    const filterValue = inputH.value.toLowerCase();

    for (let i = 0; i < filterItems.length; i++) {
      const item = filterItems[i];
      const itemText = item.textContent || item.innerText;

      if (itemText.toLowerCase().indexOf(filterValue) > -1) {
        item.style.display = "";
        item.parentElement.style.display = "";
      } else {
        item.style.display = "none";
        item.parentElement.style.display = "none";
      }
    }
    for (let i = 0; i < filterItemsMob.length; i++) {
      const item = filterItemsMob[i];
      const itemText = item.textContent || item.innerText;

      if (itemText.toLowerCase().indexOf(filterValue) > -1) {
        item.style.display = "";
        item.parentElement.style.display = "";
      } else {
        item.style.display = "none";
        item.parentElement.style.display = "none";
      }
    }
  }

  console.log(inputH.outerHTML);

  inputH.addEventListener("input", handleFilterItems);
  input1.addEventListener("input", handleFilterItems);
  input2.addEventListener("input", handleFilterItems);
}

// if (document.getElementById("folderBtn")) {
//   const btn = document.getElementById("folderBtn");
//   const iconUp = document.getElementById("foldersIcon");
//   const iconDown = document.getElementById("foldersIcon2");
//   iconUp.style.display = "";
//   iconDown.style.display = "none";
//   const folders = document.getElementById("folders");
//   btn.addEventListener("click", openFolders);
//   function openFolders() {
//     if (iconUp.style.display === "none") {
//       iconUp.style.display = "";

//       iconDown.style.display = "none";
//       folders.style.display = "none";
//     } else if (iconUp.style.display === "") {
//       iconUp.style.display = "none";
//       iconDown.style.display = "";
//       folders.style.display = "";
//     }
//   }
// }

if (document.getElementById("folderBtn")) {
  const btn = document.getElementById("folderBtn");
  const iconUp = document.getElementById("foldersIcon");
  const iconDown = document.getElementById("foldersIcon2");
  iconUp.style.display = "";
  iconDown.style.display = "none";
  const folders = document.getElementById("folders");
  btn.addEventListener("click", openFolders);
  function openFolders() {
    if (iconUp.style.display === "none") {
      iconUp.style.display = "";

      iconDown.style.display = "none";
      folders.classList.toggle("folders-active");
    } else if (iconUp.style.display === "") {
      iconUp.style.display = "none";
      iconDown.style.display = "";
      folders.classList.toggle("folders-active");
    }
  }
}

if (document.getElementById("filterInputTasks")) {
  const filterInputTasks = document.getElementById("filterInputTasks");
  const items = document.getElementsByClassName("todo-card");

  filterInputTasks.addEventListener("input", handleFilterItems);

  function handleFilterItems() {
    const filterValue = filterInputTasks.value.toLowerCase();

    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      const itemText = item.querySelector("p").innerText.toLowerCase();

      if (itemText.includes(filterValue)) {
        item.style.display = "block";
      } else {
        item.style.display = "none";
      }
    }
  }
}

if (document.getElementById("filterBtn")) {
  const filterBtn = document.getElementById("filterBtn");
  const filterContainer = document.getElementById("filterContainer");
  const filterDivUp = document.getElementById("filterDivUp");
  const filterDivDown = document.getElementById("filterDivDown");

  filterBtn.addEventListener("click", drDisplay);
  function drDisplay() {
    if (filterContainer.style.display === "none") {
      filterContainer.style.display = "";
      filterDivUp.style.display = "none";
      filterDivDown.style.display = "";
    } else if (filterContainer.style.display === "") {
      filterContainer.style.display = "none";
      filterDivUp.style.display = "";
      filterDivDown.style.display = "none";
    }
  }
}

if (document.getElementById("foldersMobBtn")) {
  var btn = document.getElementById("foldersMobBtn");
  var iconUp = document.getElementById("foldersIconUpMob");
  var iconDown = document.getElementById("foldersIconDownMob");
  var folders = document.getElementById("mob-folders");
  btn.addEventListener("click", mobFolders);
  function mobFolders() {
    console.log(1);
    if (folders.style.display === "none") {
      folders.style.display = "";
      iconUp.style.display = "none";
      iconDown.style.display = "";
    } else if (folders.style.display === "") {
      folders.style.display = "none";
      iconUp.style.display = "";
      iconDown.style.display = "none";
    }
  }
}
