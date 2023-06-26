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

function messageOk() {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("messageOk", "shadow");
    const heading = document.createElement("h4");
    heading.textContent = "Completed";
    messageDiv.appendChild(heading);
    document.body.appendChild(messageDiv);
    setTimeout(function () {
        messageDiv.remove();
    }, 1500);
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

if (document.getElementById("dtLoc")) {
    var dtLoc = document.getElementById("dtLoc");
    dtLoc.value = formattedDateTime;
    dtLoc.min = formattedDateTime;
}

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
    });

    // Event listener for input 2
    input2.addEventListener("input", function () {
        sharedValue = input2.value;
        input1.value = sharedValue;
        inputH.value = sharedValue;
    });
} catch {}

if (document.getElementById("foldersHidden")) {
    // const filterInput = document.getElementById("filterInput");
    const divContainer = document.getElementById("divContainer");
    const filterItems = divContainer.getElementsByClassName("filterItem");
    const divContainerMob = document.getElementById("divContainerMob");
    const filterItemsMob = divContainerMob.getElementsByClassName("filterItem");

    function handleFilterItems() {
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

// if (document.getElementById("folderBtn")) {
//     const btn = document.getElementById("folderBtn");
//     const iconUp = document.getElementById("foldersIcon");
//     const iconDown = document.getElementById("foldersIcon2");
//     iconUp.style.display = "";
//     iconDown.style.display = "none";
//     const folders = document.getElementById("folders");
//     btn.addEventListener("click", openFolders);

//     function openFolders() {
//         if (iconUp.style.display === "none") {
//             iconUp.style.display = "";

//             iconDown.style.display = "none";
//             folders.classList.toggle("folders-active");
//         } else if (iconUp.style.display === "") {
//             iconUp.style.display = "none";
//             iconDown.style.display = "";
//             folders.classList.toggle("folders-active");
//         }
//     }
// }

// if (document.getElementById("foldersMobBtn")) {
//     var btn = document.getElementById("foldersMobBtn");
//     var iconUp = document.getElementById("foldersIconUpMob");
//     var iconDown = document.getElementById("foldersIconDownMob");
//     var folders = document.getElementById("mob-folders");
//     btn.addEventListener("click", mobFolders);

//     function mobFolders() {
//         if (folders.style.display === "none") {
//             folders.style.display = "";
//             iconUp.style.display = "none";
//             iconDown.style.display = "";
//         } else if (folders.style.display === "") {
//             folders.style.display = "none";
//             iconUp.style.display = "";
//             iconDown.style.display = "none";
//         }
//     }
// }

if (document.getElementById("folderBtn")) {
    const btn = document.getElementById("folderBtn");
    const iconUp = document.getElementById("foldersIcon");
    const iconDown = document.getElementById("foldersIcon2");
    const folders = document.getElementById("folders");
    btn.addEventListener("click", openFolders);

    const btnMob = document.getElementById("foldersMobBtn");
    const iconUpMob = document.getElementById("foldersIconUpMob");
    const iconDownMob = document.getElementById("foldersIconDownMob");
    const foldersMob = document.getElementById("mob-folders");
    btnMob.addEventListener("click", openFolders);

    function openFolders() {
        if (iconUp.style.display === "none") {
            iconUp.style.display = "";
            iconDown.style.display = "none";
            folders.classList.toggle("folders-active");

            iconUpMob.style.display = "";
            iconDownMob.style.display = "none";
            foldersMob.style.display = "none";
        } else if (iconUp.style.display === "") {
            iconUp.style.display = "none";
            iconDown.style.display = "";
            folders.classList.toggle("folders-active");

            iconUpMob.style.display = "none";
            iconDownMob.style.display = "";
            foldersMob.style.display = "";
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

if (document.getElementsByClassName("todo-add-submit").length > 0) {
    const btnAdd = document.getElementsByClassName("todo-add-submit")[0];
    const inputVal = document.getElementsByClassName("todo-add-text")[0];
    const container = document.getElementById("paginationContainer");
    btnAdd.addEventListener("click", addTodo);

    function addTodo(event) {
        event.preventDefault();
        const form = document.getElementById("addTodoForm");
        const inputDate =
            document.getElementsByClassName("todo-add-datetime")[0];
        const datetime = new Date(inputDate.value);

        console.log(inputDate.value);

        fetch(form.action, {
            method: form.method,
            body: new FormData(form),
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Form submission failed");
                }
            })
            .then((data) => {
                if (inputVal === "") {
                    return "Error";
                }
                const month = datetime.toLocaleString("default", {
                    month: "long",
                });
                const day = datetime.getDate();
                const year = datetime.getFullYear();
                const hours = datetime.getHours();
                const minutes = datetime.getMinutes();
                // const month = datetime.toLocaleString("default", {
                //     month: "long",
                // });
                // const day = datetime.getDate();
                // const year = datetime.getFullYear();
                var newDiv = document.createElement("div");
                newDiv.className = "todo-card";
                if (inputDate.value !== "") {
                    newDiv.innerHTML = `
                    <div class="testo">
                        <input type="checkbox" name="" id="checkbox-id" />
                        <label for="checkbox-id">Completed</label>
                        <div class="until-div">
                            <button class="position-relative" onclick="untilDropdown(this)">
                                Until<i class="fa-solid fa-caret-down mx-2"></i>
                            </button>
                            <div class="todo-until shadow" style="display: none">
                                ${month} ${day}, ${year}<br />
                                ${hours}:${minutes}<br />
                            </div>
                        </div>
                        <div class="">
                            <button class="btn-dr" onclick="untilDropdown(this)">
                                <i class="fa-solid fa-ellipsis-vertical fa-lg"></i>
                            </button>
                            <div class="options shadow" style="display: none">
                                <span><a href="" id="editBtn">Edit</a></span>
                                <span><a href="" id="addToFolderBtn(${data.pk})">Add to Folder</a></span>
                                <span onclick="toDelete(this, ${data.pk})"><a id="deleteBtn">Delete</a></span>

                            </div>
                        </div>
                    </div>
                    <p class="my-auto">${inputVal.value}</p>
                `;
                } else {
                    newDiv.innerHTML = `
                    <div class="testo">
                        <input type="checkbox" name="" id="checkbox-id" />
                        <label for="checkbox-id">Completed</label>

                        <div class="">
                            <button class="btn-dr" onclick="untilDropdown(this)">
                                <i class="fa-solid fa-ellipsis-vertical fa-lg"></i>
                            </button>
                            <div class="options shadow" style="display: none">
                                <span><a href="" id="editBtn">Edit</a></span>
                                <span><a href="" id="addToFolderBtn(${data.pk})">Add to Folder</a></span>
                                <span onclick="toDelete(this, ${data.pk})"><a id="deleteBtn">Delete</a></span>
                            </div>
                        </div>
                    </div>
                    <p class="my-auto">${inputVal.value}</p>
                `;
                }
                document.addEventListener("click", outsideClickHandler);

                // Insert the newDiv as the first child of the container
                if (container.firstChild) {
                    container.insertBefore(newDiv, container.firstChild);
                } else {
                    container.appendChild(newDiv);
                }
                inputVal.value = "";
            })
            .catch((error) => {
                // Handle any errors that occur during submission
                console.error(error);
            });
    }
}

if (document.getElementsByClassName("specBtn")) {
    const btn = document.getElementsByClassName("specBtn")[0];
    const inputDate = document.getElementById("dtLoc");
    var inputDateValue = inputDate.value;
    inputDate.value = "";
    btn.addEventListener("click", function (event) {
        event.preventDefault();
    });
    btn.addEventListener("click", addDateBtn);

    function addDateBtn() {
        if (btn.style.display === "") {
            btn.style.display = "none";
            inputDate.style.display = "";
        }
    }
}

function checkbox(cbInput) {
    let state = cbInput.checked;
    const url = `/api/edit-cb/${cbInput.value}/${state}`;
    fetch(url, {
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            if (response.status === 401) {
                window.location.replace("/login/");
                return;
            }
            if (response.ok) {
                return response.text();
            } else {
                throw new Error("Failed to like the post.");
            }
        })

        .catch((error) => {
            console.error("An error occurred while liking the post:", error);
        });
}

try {
    const inp = document.getElementById("folderCreateInput");
    const inp2 = document.getElementById("folderCreateInput2");
    const hFolderInput = document.getElementById("hFolderInput");
    var sharedValueF = "";
    inp.addEventListener("input", function () {
        sharedValueF = inp.value;
        inp2.value = sharedValueF;
        hFolderInput.value = sharedValueF;
        checkInput();
    });

    // Event listener for input 2
    inp2.addEventListener("input", function () {
        sharedValueF = inp2.value;
        inp.value = sharedValueF;
        hFolderInput.value = sharedValueF;
        checkInput();
    });
    function checkInput() {
        if (hFolderInput.value === "") {
            inp.nextElementSibling.disabled = true;
            inp2.nextElementSibling.disabled = true;
        } else {
            inp.nextElementSibling.disabled = false;
            inp2.nextElementSibling.disabled = false;
        }
    }
} catch {}

function removeHiddenInput() {
    const inp = document.getElementById("folderCreateInput");
    const inp2 = document.getElementById("folderCreateInput2");
    const hFolderInput = document.getElementById("hFolderInput");
    inp.value = "";
    inp2.value = "";
    hFolderInput.value = "";
}

function addFolderFunction(btn) {
    const divContainer = document.getElementById("divContainer");
    const divContainerMob = document.getElementById("divContainerMob");
    const hFolderInput = document.getElementById("hFolderInput");

    const createFolderLink = (folderTitle) => {
        return `<a href="/folder/${hFolderInput.value}" class="filterItem">${folderTitle}</a>`;
    };

    const folderTitle = hFolderInput.value;

    const fDiv = document.createElement("div");
    fDiv.innerHTML = createFolderLink(folderTitle);
    const sDiv = document.createElement("div");
    sDiv.innerHTML = createFolderLink(folderTitle);

    divContainer.appendChild(fDiv);
    divContainerMob.appendChild(sDiv);

    // console.log(divContainer.offsetParent);
    // const par = divContainer.offsetParent

    if (folderTitle !== "") {
        sendFolderForm(folderTitle);
        removeHiddenInput();
    }
}

function sendFolderForm(folderTitle) {
    const url = "/api/create-folder/";
    const requestData = {
        folderTitle: folderTitle,
    };

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(requestData),
    })
        .then((response) => {
            // Handle the response here (if needed)
        })
        .catch((error) => {
            // Handle the error here
            console.log("111");
            console.error("Error:", error);
        });
}

function getCookie(name) {
    const cookieValue = document.cookie.match(
        "(^|;)\\s*" + name + "\\s*=\\s*([^;]+)"
    );
    return cookieValue ? cookieValue.pop() : "";
}

function toDelete(btn, id) {
    const todoCard =
        btn.parentElement.parentElement.parentElement.parentElement;
    const todoTitle = todoCard.querySelector(".my-auto").textContent;
    confirmation(todoTitle).then((confirmed) => {
        if (confirmed) {
            const url = `/api/delete-todo/${id}`;
            const todoCard =
                btn.parentElement.parentElement.parentElement.parentElement;
            fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            })
                .then((response) => {
                    if (response.status === 200) {
                        todoCard.remove();
                        messageOk();
                    }
                    // Handle the response here (if needed)
                })
                .catch((error) => {
                    // Handle any errors here
                });
        }
    });
}

if (document.getElementsByClassName("removeFolder")) {
    const removeFolderButtons = document.getElementsByClassName("removeFolder");

    for (let i = 0; i < removeFolderButtons.length; i++) {
        const button = removeFolderButtons[i];
        const f_id = button.previousElementSibling.id.split("_")[1];
        button.addEventListener("click", function () {
            const url = `/api/delete-folder/${f_id}`;

            fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            }).then((response) => {
                button.parentElement.remove();
            });
        });
    }
}

function confirmation(title) {
    return new Promise((resolve) => {
        // Create the main container div
        const containerDiv = document.createElement("div");
        containerDiv.classList.add("confirmation", "shadow");

        // Create the <h4> element
        const heading = document.createElement("h4");
        heading.innerHTML = `Are you sure you want to delete<br><br><span>${title}?</span>`;

        // Create the div for the buttons
        const buttonDiv = document.createElement("div");

        // Create the Confirm button
        const confirmButton = document.createElement("button");
        confirmButton.textContent = "Confirm";
        buttonDiv.appendChild(confirmButton);

        // Create the Cancel button
        const cancelButton = document.createElement("button");
        cancelButton.textContent = "Cancel";
        buttonDiv.appendChild(cancelButton);

        // Append the heading and button div to the main container div
        containerDiv.appendChild(heading);
        containerDiv.appendChild(buttonDiv);

        // Append the container div to the document body or any other desired parent element
        document.body.appendChild(containerDiv);

        // Add a mousedown event listener to the document
        document.addEventListener("mousedown", function (event) {
            // Check if the clicked element is outside the containerDiv
            if (!containerDiv.contains(event.target)) {
                containerDiv.remove();
                resolve(false);
            }
        });

        confirmButton.addEventListener("click", function () {
            containerDiv.remove();
            resolve(true);
        });

        cancelButton.addEventListener("click", function () {
            containerDiv.remove();
            resolve(false);
        });
    });
}

async function fetchFolders(todoId) {
    const url = "/api/folders/";
    const response = await fetch(url);
    const jsonData = await response.json();
    const folderTitles = jsonData.map((item) => item.folder_title);
    const folderIds = jsonData.map((item) => item.id);
    createFolderDiv(folderTitles, folderIds, todoId);
}
function addToFolderRequest(span, todoId, folderId) {
    const addToFolderUrl = `/api/add-to-folder/${folderId}/${todoId}/`;
    fetch(addToFolderUrl, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    }).then((response) => {
        span.parentElement.parentElement.parentElement.remove();
        messageOk();
    });
}

function createFolderDiv(folderList, folderIds, todoId) {
    const folderDiv = document.createElement("div");
    folderDiv.classList.add("addFolders", "shadow");

    const heading = document.createElement("h4");
    heading.textContent = "Folders";
    folderDiv.appendChild(heading);

    const folderContainerDiv = document.createElement("div");
    folderContainerDiv.classList.add("folderContainer");
    folderDiv.appendChild(folderContainerDiv);

    const folderListDiv = document.createElement("div");
    folderListDiv.classList.add("folderList");
    folderContainerDiv.appendChild(folderListDiv);

    folderList.forEach((folderName, index) => {
        const span = document.createElement("span");
        span.textContent = folderName;
        folderListDiv.appendChild(span);

        const folderId = folderIds[index];
        span.addEventListener("click", function () {
            addToFolderRequest(span, todoId, folderId);
        });
    });

    const inputFolderDiv = document.createElement("div");
    inputFolderDiv.classList.add("inputFolderDiv");
    folderDiv.appendChild(inputFolderDiv);

    const inputField = document.createElement("input");
    inputField.setAttribute("type", "text");
    inputField.setAttribute("placeholder", "Filter");
    inputFolderDiv.appendChild(inputField);

    document.addEventListener("click", function (event) {
        if (!folderDiv.contains(event.target)) {
            folderDiv.remove();
        }
    });

    inputField.addEventListener("input", function () {
        const filterText = inputField.value.toLowerCase();
        const spanElements = folderListDiv.getElementsByTagName("span");

        for (let i = 0; i < spanElements.length; i++) {
            const span = spanElements[i];
            const folderName = span.textContent.toLowerCase();

            if (folderName.includes(filterText)) {
                span.style.display = "block";
            } else {
                span.style.display = "none";
            }
        }
    });

    document.body.appendChild(folderDiv);
}

function smWrong(text) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("messageWrong", "shadow");
    const heading = document.createElement("h4");
    heading.textContent = text;
    messageDiv.appendChild(heading);
    document.body.appendChild(messageDiv);
    setTimeout(function () {
        messageDiv.remove();
    }, 1500);
}

function editTodo(btn, todo_id) {
    const url = "/api/edit-todo/";
    const todoText =
        btn.parentElement.parentElement.parentElement.nextElementSibling;

    const body = document.querySelector("body");
    const div = document.createElement("div");
    div.className = "editTodoContainer shadow";
    div.innerHTML = `
        <div class="textTodoContainer">
        <textarea name="editTodo" id="" cols="30" rows="10">${todoText.innerText}</textarea>
            <div class="closeDiv"><i class="fa-solid fa-xmark"></i></div>
            <input type="hidden" name="id" value="${todo_id}">
            <div class="btnIn">
                <button id="saveBtn">Save</button>
            </div>
        </div>
    `;

    const closeButton = div.querySelector(".closeDiv");
    closeButton.addEventListener("click", function () {
        div.remove();
    });
    const saveButton = div.querySelector("#saveBtn");
    saveButton.addEventListener("click", function () {
        const input = div.firstElementChild.firstElementChild.value;

        if (input === "") {
            console.log(input);
            return smWrong("Field should not be empty");
        } else if (input === todoText.innerText) {
            div.remove();
            return smWrong("Todo not changed.");
        }
        const formData = new FormData();
        formData.append("id", todo_id);
        formData.append("editTodo", input);

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: formData,
        })
            .then((response) => {
                // Handle the response here (if needed)
            })
            .catch((error) => {
                // Handle any errors here
            });

        todoText.innerHTML = input;
        messageOk();
        div.remove();
        // Handle save button click here
    });

    body.appendChild(div);

    document.addEventListener("click", function handleClickOutsideBox(event) {
        if (!div.contains(event.target) && event.target !== btn) {
            div.remove();
        }
    });
}

const links = document.getElementsByClassName("page-link");
const currentUrl = new URL(window.location.href);

const isCompleted = currentUrl.searchParams.has("completed");
const isUncompleted = currentUrl.searchParams.has("uncompleted");

for (let i = 0; i < links.length; i++) {
    const link = links[i];
    const href = link.getAttribute("href");
    const url = new URL(href, window.location.href);

    url.searchParams.delete("completed");
    url.searchParams.delete("uncompleted");

    if (isCompleted) {
        url.searchParams.set("completed", "");
    } else if (isUncompleted) {
        url.searchParams.set("uncompleted", "");
    }

    link.setAttribute("href", url.toString());
}
