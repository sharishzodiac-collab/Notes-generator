const generateBtn = document.getElementById("generateBtn");
const transcriptBox = document.getElementById("transcript");
const notesBox = document.getElementById("notes");
//this button uses anonymous fnc.
generateBtn.addEventListener("click", async () => {
    //async-asynchronous function allow the function to run parallel,without blocking the web.

    const transcript = transcriptBox.value.trim();

    //trim-helps to trim the empty spaces in the start and the end of the string.

    if (!transcript)//false 
    {
        alert("Enter transcript Before generating notes.");
        return;
    }

    // Show loading message in the  interface
    notesBox.textContent = "Notes generation in progress...";

    try {
        //await-it is used in async fnc,it make the function proceed untill if fetched,waits
        //fetch -inbuild function helps to communicate,its has methods like post,get,put,patch,delete
        const response = await fetch("/generate-notes", {
            method: "POST",
        //gives additional info of input
            headers: {
                "Content-Type": "application/json"
            },
        
            body: JSON.stringify({
                transcript: transcript
            })
        });
        //convert the transcript into json type

        if (!response.ok) //false
            {
            throw new Error("Server error: " + response.status);
        }

        const data = await response.json();

        // Display the notes produced by gemini
        notesBox.textContent = data.notes;

    } catch (error) {

        console.error(error);

        notesBox.textContent =
            "Something went wrong.check whether the backend is running.";
    }
});


//initiate in terminal by "python -m uvicorn app:app --reload"