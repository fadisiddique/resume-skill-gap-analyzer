const analyzeBtn = document.getElementById("analyzeBtn");
const loader = document.getElementById("loader");
const resultBox = document.getElementById("result");

analyzeBtn.addEventListener("click", async () => {
  const resumeFile = document.getElementById("resume").files[0];
  const JdText = document.getElementById("jd").value;

  if (!resumeFile || !JdText.trim()) {
    alert("Please upload resume file and input Job description");
    return;
  }


  loader.style.display = "block";
  resultBox.style.display = "none";
  analyzeBtn.disabled = true;
  analyzeBtn.innerText = "Analyzing...";

  const formData = new FormData();
  formData.append("resume_file", resumeFile);
  formData.append("jd_text", JdText);

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData
    });

    if (!response.ok) throw new Error("Server error");

    const data = await response.json();


    document.getElementById("score").innerText =
      `Match Score: ${data["match Score"].toFixed(2)}%`;

    const matchedList = document.getElementById("matched");
    const missingList = document.getElementById("missing");
    matchedList.innerHTML = "";
    missingList.innerHTML = "";

    data["matched skills"].forEach(skill => {
      const li = document.createElement("li");
      li.innerText = skill;
      matchedList.appendChild(li);
    });

    data["missing skills"].forEach(skill => {
      const li = document.createElement("li");
      li.innerText = skill;
      missingList.appendChild(li);
    });

    resultBox.style.display = "block";
  } catch (error) {
    console.error(error);
    alert("Something went wrong. Check backend logs.");
  } finally {

    loader.style.display = "none";
    analyzeBtn.disabled = false;
    analyzeBtn.innerText = "Analyze Resume";
  }
});
const resumeInput = document.getElementById("resume");
const uploadText = document.getElementById("uploadText");
const uploadBox = document.querySelector(".upload-box");

resumeInput.addEventListener("change", () => {
  if (resumeInput.files.length > 0) {
    uploadText.innerHTML = `
      <strong>File uploaded</strong><br>
      <small>${resumeInput.files[0].name}</small>
    `;
    uploadBox.style.borderColor = "#22c55e";
  }
});