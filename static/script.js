  var rf,sb;
  $(document).ready(function(){
    
    refundata()
    mydata()
    $('#year-month').hide()
    $('#subcategry').hide()
    $('#cattable').DataTable();
    let d= new Date();
    let date= d.getFullYear();
    var years;
    for(x=date; x>=2015;x--){
       years+=`<option value="${x}">${x}</option>`;
    }
    $('#year').append(years)
    //chart data form backhand start
    var dates = [];
    var amounts = [];
    $.ajax({
      url:'chartview',
      type:'GET',
      data:{year:d.getFullYear()},
      success:function(data){
      let datas=eval(data)
      for(x=0;x<datas.length;x++){
       dates.push(datas[x].date);
       amounts.push(datas[x].amount);
      }
      mychart(dates,amounts);
      datas=[];
      amounts=[];
    }
      });
      var yearlist;
      var monthlist;
      //Month Names
      const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];
      //Year show in slect box start code 
       for(x=date;x>=2015;x--){
       yearlist+=`<option value="${x}">${x}</option>`;
       }
       $('#yearselect').append(yearlist)
      //Year show in slect box start end
      for(x=0;x<12;x++){
        monthlist+=`<option value="${x+1}">${monthNames[x]}</option>`;
        }
        $('#monthselect').append(monthlist);
      // select Month List  end
      viewchart(2020)
  });
  function viewchart(e){
    var dates = [];
    var amounts = [];
    $.ajax({
      url:'chartview',
      type:'GET',
      data:{year:e},
      success:function(data){
      let datas=eval(data)
      for(x=0;x<datas.length;x++){
        
       dates.push(datas[x].date);
       amounts.push(datas[x].amount);
      }
      mychart(dates,amounts);
       datas=[];
       amounts=[];
    }
      });
  }
  var subtotal ,maintotal,refundamount;
  function mychart(dates,amounts){
  
  var ctx = document.getElementById('chartBig1').getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'line',

      data: {
          labels:dates,
          datasets: [{
              label: 'Monthly spends',
              data:amounts,
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)'
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)'
              ],
              borderWidth: 1,
             
          }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero: true
                  }
                  
              }]
          }
      }
  });
  }
 
  function mydata(){
   
    const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];
  var table;
    var total=0;
    var cat=$('#category').val();
    var month=$('#monthselect').val();
    
    var year=$('#yearselect').val();
    if(cat==""){
      cat='b'
    }
    if(month==""){
      month='a';
    }
    if(year==""){
      year='a';
    }
    if(category==""){
      year='a';
    }
    $.ajax({
      url:'homedata',
      type:'GET',
      data:{
        month:month,
        year:year,
        cat:cat,
      },
      success:function(data){
        refundata()
        const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];
        var datas= eval(data);
        var xdata=[];
        var rawdata=[];
        for(x=0;x<datas.length;x++){
          xdata.push(datas[x].z)
          rawdata.push(datas[x].mydata)
        }
        var filtered = rawdata.filter(function (el) {
          return el != null;
        });
        var eachmonth = xdata.filter(function (el) {
          return el != null;
        });
        var tota=0;
        if(year !='a' && month=="a" && cat=='b'){
      
        
          var table;
         
         for(x=0;x<filtered.length;x++){
          $('#year-month').show()
          $('#subcategry').hide()
        
      

       
       total+=filtered[x][3];
     table+=`
       <tr>
         <td>${monthNames[filtered[x][1]-1]}-${filtered[x][0]}</td>
         <td>${filtered[x][2]}</td>
         <td>${Number(filtered[x][3]).toFixed(2)}</td>
        
       </tr>
     `;
     
     
         }
      $('#showyear').text(`${year}`)

      // year each month calculation start
    
    
      var monthlyreport;
      $('#b-report').text("Monthly Report")
      for(x=0;x<eachmonth.length;x++){
         console.log(eachmonth[x])
         monthlyreport+=`
          
          <tr>
            <td>${eachmonth[x][0]}-${monthNames[eachmonth[x][1]-1]}</td>
            <td>${Number(eachmonth[x][2]).toFixed(2)}</td>
          </tr>
          `;
      }
      // year each month calculation end
      //  end year condition
      $('#mydata').empty();
      $('#monthlydata').empty();
        }
        // monthly base report condition start
        else if(year =='a' && month !="a" && cat=='b'){
          $('#year-month').hide()
          $('#subcategry').hide()
          alert("Please Select Year")
        }
        else if(year !='a' && month !="a" && cat=='b'){
          table="";
          $('#year-month').show()
        $('#subcategry').hide()
       $('#showyear').text(`${monthNames[month-1]}-${year}`)
       
        $('#b-report').text("Daily Report")
        var table;
      
       for(x=0;x<filtered.length;x++){
          total+=filtered[x][4];
        table+=`
     <tr>
       <td>${monthNames[filtered[x][1]-1]}-${filtered[x][2]}-${filtered[x][0]}</td>
       <td>${filtered[x][3]}</td>
       <td>${Number(filtered[x][4]).toFixed(2)}</td>
      
     </tr>
   `;
   
       }
       var monthlyreport;
      // $('#b-report').text("Monthly Report")

      for(x=0;x<eachmonth.length;x++){

     
         monthlyreport+=`
          
          <tr>
            <td>${eachmonth[x][0]}-${eachmonth[x][1]}-${monthNames[eachmonth[x][2]-1]}</td>
            <td>${Number(eachmonth[x][3]).toFixed(2)}</td>
          </tr>
          `;
      }
       }
       else if(year !='a' && month =="a" && cat !='b'){
        
        //  baloch
        $('#year-month').show()
        $('#subcategry').show()
      
       
      // alert(alldata[x].amount)
       for(x=0;x<filtered.length;x++){ 
        if(filtered[x][4]>0){
          total+=filtered[x][4];
      
        table+=`
        <tr>
          <td>${ monthNames[filtered[x][2]-1]}-${filtered[x][1]}-${filtered[x][3]}</td>
          <td>${filtered[x][0]}</td>
          <td>${filtered[x][4]}</td>
         
        </tr>
      `;
      }
    }

    // monthly report show
    $('#showyear').text(`${year}`)
    $('#year-month').show();
    $('#limited').hide();

      // year each month calculation start
    
      console.log("this is ",eachmonth)
      var monthlyreport;
      $('#b-report').text("Monthly Report")
      for(x=0;x<eachmonth.length;x++){
         
         monthlyreport+=`
          
          <tr>
            <td>${eachmonth[x][1]}-${monthNames[eachmonth[x][0]-1]}</td>
            <td>${Number(eachmonth[x][2]).toFixed(2)}</td>
          </tr>
          `;
      }
      // year each month calculation end
      //  end year condition
   

    $('#subdata').html(table)
    $('#subtotal').html(Number(total).toFixed(3))
      sb=total;
    
      }
        // monthly base report condition end
        // footer data start
   
        $('#total').html(Number(total).toFixed(2))
        $('#monthlydata').append(monthlyreport);
       $('#mydata').html(table)  
      //  $('#mydata').empty();
      // $('#monthlydata').empty();
        
      //  footer data end
      }
      
    });
   
        //code start
        $.ajax({
            url:'homedata',
            type:'GET',
            data:{
              month:month,
              year:year,
              cat:cat,
            },
            success:function(data){
             
              var table;
              let alldata=eval(data);
          
              let rufundamount=0;
              for(x=0;x<alldata.length;x++){
                var CDate = new Date(alldata[x].date);
                var d=CDate.getDate();
                var m=monthNames[CDate.getMonth()];
                var y=CDate.getFullYear();
                //var CDate = (new Date(alldata[x].date)).format("yyyy-dd-mm");
                if(year !='a' && month !="a" && cat !='b'){
                 
                  $('#year-month').hide()
                  $('#subcategry').show()
                if(alldata[x].amount>0){
                total+=alldata[x].amount;
                // sb+=alldata[x].amount;
                table+=`
                  <tr>
                    <td>${m}-${d}-${y}</td>
                    <td>${alldata[x].Sub}</td>
                    <td>${alldata[x].amount}</td>
                   
                  </tr>
                `;
                }
              sb=total;
             
              }
             
              // code start
              else if(year =='a' && month =="a" && cat !='b'){
                $('#year-month').hide()
                $('#subcategry').show()
              if(alldata[x].amount>0){
              total+=alldata[x].amount;
              table+=`
                <tr>
                  <td>${d}-${m}-${y}</td>
                  <td>${alldata[x].Sub}</td>
                  <td>${alldata[x].amount}</td>
                 
                </tr>
              `;
              }
              else{
                rufundamount+=alldata[x].amount
              }
              }
              // ebd
              }
           
             
              $('#subdata').html(table)
              $('#subtotal').html(Number(total).toFixed(3))
              //  $('#totalamount').html(Number(maintotal).toFixed(3))
              return total;
            
            }
          });
        
      
        //code end

     























        
        $('#subdata').empty()
        $('#subtotal').empty()
         $('#totalamount').empty()
         $('#total').empty()
         $('#monthlydata').empty();
        $('#mydata').empty()
        table=null;  
        total=null;``
        
    
    }
    monthlyreport=null;
   

// function refund start
function refundata(){
 // MY FUNCTION START
 const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];
var table;
var total=0;
var cat=$('#category').val();
var month=$('#monthselect').val();

var year=$('#yearselect').val();
if(cat==""){
  cat='b'
}
if(month==""){
  month='a';
}
if(year==""){
  year='a';
}
if(category==""){
  year='a';
}
$.ajax({
  url:'refunddata',
  type:'GET',
  data:{
    month:month,
    year:year,
    cat:cat,
  },
  success:function(data){
    let alldata=eval(data);
     
    for(x=0;x<alldata.length;x++){
      var CDate = new Date(alldata[x].Date);
      var d=CDate.getDate();
      var m=monthNames[CDate.getMonth()];
      var y=CDate.getFullYear();
   
      total+=alldata[x].Amount;
      
      table+=`
        <tr>
          <td>${m}-${d}-${y}</td>
          <td>${alldata[x].DoingBusinessAs}</td>
          <td>${alldata[x].Amount}</td>
         
        </tr>
      `;
    

  }
    $('#rmydata').html(table)
    $('#rtotal').html(total)
     var maintotals=total+sb;
    $('#totalamount').html(Number(maintotals).toFixed(3))
    // maintotal=subtotal+(total)
  
  }
});

$('#rmydata').empty()
$('#rtotal').empty()
// MY FUNCTION END 

}

// function refund end