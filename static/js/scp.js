const contanier=document.getElementById("contanier");
        var file_name=""
	
      //add();
        var last=1
        function createcell()
        {
           const cell=document.createElement("div");
           cell.className="cell";
           last+=1
           cell.id="cell"+last
           newinput=document.createElement("textarea");

           runbtn=document.createElement("button");
           
           
           runbtn.onclick=()=>run(cell);
          //runbtn.href=()=>"/runcode?code="+cell.textarea.value;

           above=document.createElement("button");
           above.onclick=()=>insert_above(cell);

           below=document.createElement("button");
           below.onclick=()=>insert_below(cell);

           
            output=document.createElement("pre");
			dele=document.createElement("button");
			dele.onclick=()=>dele_cell(cell);
            
           runbtn.textContent="run";
        above.textContent="insert_above";
        below.textContent="insert_below";
		dele.textContent="delete cell";

           cell.appendChild(newinput);
           cell.appendChild(runbtn);
           cell.appendChild(above);
            cell.appendChild(below);
			cell.appendChild(dele);
            cell.appendChild(output);
			
           return cell;

           


        }
		
		
    
        function add()
        {
        document.getElementById("contanier").appendChild(createcell());
        
        }
		function dele_cell(cell)
		{
		cell.remove()
		}
        function insert_above(cell)
        {
            newcell=createcell();
            //cell.parentNode.insertBefore(newcell,lcell);
            cell.parentNode.insertBefore(newcell,cell);
        }

            function insert_below(cell)
        {
            newcell=createcell();
            //cell.parentNode.insertBefore(newcell,lcell);
            cell.parentNode.insertBefore(newcell,cell.nextSibling);
        }
		
        async function run(cell)
        {
            
            data=cell.querySelector("textarea").value;
            
           let response= await fetch("/run_now", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({code:data})
            });
            let res= await response.json();
            console.log(res.output)
          
            cell.querySelector("pre").innerHTML=res.output;

            }

           
            
        
        function save()
        {
		
          const input_v = Array.from(document.querySelectorAll(".cell textarea")).map(t => t.value);
          const output_v = Array.from(document.querySelectorAll(".cell pre")).map(t => t.innerHTML);
		  console.log(file_name)
		  // Send to Flask
		  console.log("pass 1")
		  console.log(file_name)
           fetch("/save_data", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({inp:input_v,out:output_v,name:file_name})
            })
            .then(res => res.json())
			.then(res=>alert("file saved"))
            
        }
        
       
        function open()
        {
            var out={{out | tojson}}
            var inp={{inp | tojson}}
			var file_temp={{file | tojson}}
			console.log(file_temp)
			if(file_temp===null)
			{
			
			
			
		
				file_name=window.prompt("enter name \n*it should not be empty \n*it should contain only alpha numeric char")
				if(file_name=="")
				{
				alert("file name should not be empty")
				window.location.href='\open'
				}
				else if(!/^[a-zA-Z0-9]+$/.test(file_name))
				{
				alert("it should containn only alpha numeric charater")
				window.location.href='\open'
				}
				if(file_name)
				{
					save();
					fetch('\open_file?filename='+file_name)
				}

				
			console.log("the name is 1",file_name)
			add()
			
			}
			else
			{
			file_name=JSON.stringify(file_temp)
			
			
            for(let i=0;i<inp.length;i++)
            {
            add();
            cell_val=document.getElementById("cell"+last)
            cell_val.querySelector("textarea").value=inp[i]
            cell_val.querySelector("pre").textContent=out[i]

        }
		
		
		}
		}
open()