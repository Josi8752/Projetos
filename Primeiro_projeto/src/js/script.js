const productEx = {
     id:0,
nome: "Combo Whopper",
preco: 32.90,
image: "./src/assets/combo_whopper.png"
}


const listProducts = document.querySelector(".listProducts")

function cardosProduct (produto){
  const tagLi = document.createElement("li")
tagLi.classList.add("cardProduct")

tagLi.innerHTML = `
<img src="src/assets/whopper_rodeio.png" 
                alt="whopper_rodeio">
                <h3>Combo Whopper Rodeio</h3>
                <p> R$ 38.40</p>
            <button type="button">Adicionar</button>
`
listProducts.appendChild(tagLi)

}



