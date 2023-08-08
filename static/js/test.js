fetch("tech_ofs.json")
  .then(response => response.json())
  .then(json => console.log(json));