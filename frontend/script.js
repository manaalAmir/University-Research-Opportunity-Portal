
const API_URL = "http://127.0.0.1:5000/api/opportunities";

const form = document.getElementById("opportunity-form");
const list = document.getElementById("opportunities-list");
const formMessage = document.getElementById("form-message");
const listMessage = document.getElementById("list-message");
const formTitle = document.getElementById("form-title");
const submitButton = document.getElementById("submit-button");
const cancelButton = document.getElementById("cancel-button");

let editingId = null;

async function loadOpportunities() {
    listMessage.textContent = "Loading opportunities...";
    list.replaceChildren();

    try {
        const response = await fetch(API_URL);
        const opportunities = await response.json();

        if (!response.ok) {
            throw new Error(opportunities.error || "Could not load opportunities.");
        }

        listMessage.textContent = opportunities.length
            ? `${opportunities.length} opportunity/opportunities found.`
            : "No opportunities found. Add one using the form.";

        opportunities.forEach(createOpportunityCard);
    } catch (error) {
        listMessage.textContent =
            "Could not connect to the API. Make sure Flask is running.";
    }
}

function addTextElement(parent, tag, text, className = "") {
    const element = document.createElement(tag);
    element.textContent = text;

    if (className) {
        element.className = className;
    }

    parent.appendChild(element);
    return element;
}

function createOpportunityCard(opportunity) {
    const card = document.createElement("article");
    card.className = "opportunity-card";

    addTextElement(card, "h3", opportunity.ResearchTitle);
    addTextElement(card, "p", opportunity.ResearchDescription);
    addTextElement(card, "p", `Research Area: ${opportunity.ResearchArea}`);
    addTextElement(card, "p", `Faculty: ${opportunity.FacultyMemberName}`);
    addTextElement(card, "p", `Department: ${opportunity.Department}`);
    addTextElement(card, "p", `Required Skills: ${opportunity.RequiredSkills}`);
    addTextElement(
        card,
        "p",
        `Available Positions: ${opportunity.NumberOfAvailablePosition}`
    );
    addTextElement(
        card,
        "p",
        `Application Deadline: ${opportunity.ApplicationDeadline}`
    );

    const statusClass = opportunity.Status === "Closed" ? "status closed" : "status";
    addTextElement(card, "span", opportunity.Status, statusClass);

    const buttons = document.createElement("div");
    buttons.className = "card-buttons";

    const editButton = document.createElement("button");
    editButton.type = "button";
    editButton.textContent = "Edit";
    editButton.addEventListener("click", () => startEditing(opportunity));

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.textContent = "Delete";
    deleteButton.className = "delete-button";
    deleteButton.addEventListener("click", () => deleteOpportunity(opportunity.ID));

    buttons.append(editButton, deleteButton);
    card.appendChild(buttons);
    list.appendChild(card);
}

function startEditing(opportunity) {
    editingId = opportunity.ID;

    for (const field of [
        "ResearchTitle",
        "ResearchDescription",
        "ResearchArea",
        "FacultyMemberName",
        "Department",
        "RequiredSkills",
        "NumberOfAvailablePosition",
        "ApplicationDeadline",
        "Status"
    ]) {
        form.elements[field].value = opportunity[field] ?? "";
    }

    formTitle.textContent = "Edit Research Opportunity";
    submitButton.textContent = "Save Changes";
    cancelButton.hidden = false;
    formMessage.textContent = "Edit the fields and save your changes.";
    form.scrollIntoView({ behavior: "smooth", block: "start" });
}

function resetForm() {
    editingId = null;
    form.reset();
    formTitle.textContent = "Add a Research Opportunity";
    submitButton.textContent = "Add Opportunity";
    cancelButton.hidden = true;
    formMessage.textContent = "";
}

cancelButton.addEventListener("click", resetForm);

document.getElementById("refresh-button")
    .addEventListener("click", loadOpportunities);

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    formMessage.textContent = "Saving...";

    const data = Object.fromEntries(new FormData(form).entries());
    data.NumberOfAvailablePosition = Number(data.NumberOfAvailablePosition);

    const isEditing = editingId !== null;
    const url = isEditing ? `${API_URL}/${editingId}` : API_URL;

    try {
        const response = await fetch(url, {
            method: isEditing ? "PUT" : "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not save opportunity.");
        }

        formMessage.textContent = result.message || "Saved successfully.";
        resetForm();
        await loadOpportunities();
    } catch (error) {
        formMessage.textContent = error.message;
    }
});

async function deleteOpportunity(id) {
    if (!confirm("Are you sure you want to delete this opportunity?")) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not delete opportunity.");
        }

        if (editingId === id) {
            resetForm();
        }

        listMessage.textContent = result.message;
        await loadOpportunities();
    } catch (error) {
        listMessage.textContent = error.message;
    }
}

loadOpportunities();
