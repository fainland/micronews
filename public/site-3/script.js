fetch('static/metadata.json')
  .then(response => response.json())
  .then(data => {
    document.title = data.title;

    document.getElementById('headline').textContent = data.title;
    document.getElementById('summary').textContent = data.summary;

    // Fill timeline list
    const timelineList = document.getElementById('timeline');
    data.timeline.forEach(item => {
      const li = document.createElement('li');
      li.textContent = item;
      timelineList.appendChild(li);
    });

    // Fill "why it matters"
    document.getElementById('why').textContent = data.why_matters;

    // Fill sources
    const sources = document.getElementById('sources');
    data.sources.forEach(src => {
      const link = document.createElement('a');
      link.href = src.url;
      link.textContent = src.label;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';

      const para = document.createElement('p');
      para.appendChild(link);
      sources.appendChild(para);
    });
  })
  .catch(error => {
    console.error('Error loading metadata:', error);
  });
