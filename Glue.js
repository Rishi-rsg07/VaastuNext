const handleFormSubmit = async (event) => {
    event.preventDefault();
    
    const payload = {
        full_name: document.getElementById('fullName').value,
        phone_string: document.getElementById('phoneString').value,
        consultation_class: document.getElementById('consultationClass').value,
        target_zone: document.getElementById('targetZone').value,
        objectives: document.getElementById('objectives').value
    };

    try {
        const response = await fetch('http://localhost:8000/api/schedule-consultation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert("Routing Request Sent!");
        }
    } catch (error) {
        console.error("Backend offline or error:", error);
    }
};

// --- WIRE THIS TO YOUR CONSULTATION FORM SUBMIT EVENT ---
async function submitConsultation(event) {
    event.preventDefault();
    
    const bookingPayload = {
        full_name: document.getElementById('fullName').value,
        phone_string: document.getElementById('phoneString').value,
        consultation_class: document.getElementById('consultationClass').value,
        target_zone: document.getElementById('targetZone').value,
        objectives: document.getElementById('objectives').value
    };

    try {
        const response = await fetch('http://localhost:8000/api/schedule-consultation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookingPayload)
        });
        
        const data = await response.json();
        if (response.ok) {
            alert("Success! Your consultation routing request has been successfully saved.");
        }
    } catch (err) {
        console.error("Communication breakdown with FastAPI server:", err);
    }
}

// --- WIRE THIS TO YOUR CHATBOT SEND INTERACTION ---
async function sendChatQuery(userTextMessage) {
    try {
        const response = await fetch('http://localhost:8000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userTextMessage })
        });
        
        const data = await response.json();
        return data.reply; // Inject this cleanly into your chat UI bubble wrapper
    } catch (err) {
        console.error("Chat backend connection failure:", err);
        return "System offline. Please check your backend instance execution status.";
    }
}