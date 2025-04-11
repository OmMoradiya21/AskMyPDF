// Handle file upload
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append("file", document.querySelector('input[type="file"]').files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById('status').textContent = data.message;
        } else {
            document.getElementById('status').textContent = data.error;
        }
    });
});

// Handle question submission
document.getElementById('questionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const question = document.getElementById('question').value;

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `question=${encodeURIComponent(question)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.answer) {
            document.getElementById('answer').textContent = 'Answer: ' + data.answer;
        } else {
            document.getElementById('answer').textContent = data.error || 'No answer found.';
        }
    });
});