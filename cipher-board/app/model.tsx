export default async function model(input: string, setRecommend: Function){
  let url = 'http://192.168.29.60:8500/recommend'  
  let payload = {
    'Input': input
  }
  console.log(input);
  await fetch(url,{method: 'POST',headers: {
    'Content-Type': 'application/json', 
  }, body: JSON.stringify(payload)}).then(response => response.json()).then(data => setRecommend(data['words']) ).catch(err => console.log('Error: ', err))
}