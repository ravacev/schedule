fetch('file:///home/ravettni/newschedule/tech_ofs.json')
    .then(response => response.json())
    .then(jsonData => {
        console.log(jsonData);
        // Now you can work with the JSON data
    })
    .catch(error => console.error('Error fetching JSON:', error));