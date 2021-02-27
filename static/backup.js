
  $(document).ready(function(){
    refundata()
    mydata()
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
        let alldata=eval(data)
        var rawdata=[]
        for(x=0;x<alldata.lenght;x++){
                rawdata.push(alldata[x].mydata)
        }
      
       
        let xdata=[];
        let rufundamount=0;
        for(x=0;x<alldata.length;x++){
             console.log(alldata[x])

          xdata.push(alldata[x].z)
          var CDate = new Date(alldata[x].date);
          var d=CDate.getDate();
          var m=monthNames[alldata[x][1-1]];
          var y=alldata[x][0];
          //var CDate = (new Date(alldata[x].date)).format("yyyy-dd-mm");
        

         
          if(year !='a' && month=="a" && cat=='b'){
            var filtered = xdata.filter(function (el) {
              return el != null;
            });
               $('#year-month').show()
               $('#subcategry').hide()
             
            $('#b-report').text("Monthly Report")
            console.log(rawdata.mydata)
            // alert(rawdata)
            total+=alldata[x].mydata[3];
          table+=`
            <tr>
              <td>${monthNames[alldata[x].mydata[1]-1]}-${alldata[x].mydata[0]}</td>
              <td>${alldata[x].mydata[2]}</td>
              <td>${Number(alldata[x].mydata[3]).toFixed(2)}</td>
             
            </tr>
          `;
          
          
          }
          else if(year !='a' && month !="a" && cat=='b'){
           
          
            $('#year-month').show()
            $('#subcategry').hide()
          if(alldata[x].Sub !=null){
            
            total+=alldata[x].amount;
            $('#b-report').text("Daily Report")
          table+=`
            <tr>
              <td>${d}-${m}-${y}</td>
              <td>${alldata[x].Sub}</td>
              <td>${alldata[x].amount}</td>
             
            </tr>
          `;
          }
          
          }
        
         
        }
        
       // let maintotal=total+(rufundamount)
       
        var filtered = xdata.filter(function (el) {
          return el != null;
        });
        var monthlyreport;
        if(year !='a' && month=="a" && cat=='b'){
           
            $('#b-report').text("Monthly Report")
        for(z=0;z<filtered.length;z++){
           var x=filtered[z][1]-1;
           
           var y=filtered[z][2];
           
          monthlyreport+=`
          
          <tr>
            <td>${monthNames[x]}</td>
            <td>${y}</td>
          </tr>
          `;
        }
      }
      else if(year !='a' && month !="a" && cat=='b'){
        $('#year-month').show()
        $('#subcategry').hide()
       $('#showyear').text(`${monthNames[month-1]}-${year}`)
        $('#b-report').text("Daily Report")
        for(z=0;z<filtered.length;z++){
           var x=filtered[z][1]-1;
           
           var y=filtered[z][3];
           
          monthlyreport+=`
          
          <tr>
            <td>${filtered[z][2]}-${monthNames[x]}</td>
            <td>${y}</td>
          </tr>
          `;
        }
      }
      else if(year =='a' && month !="a" && cat=='b'){
        $('#year-month').hide()
        $('#subcategry').hide()
        alert("Please Select year")
      }
        $('#monthlydata').append(monthlyreport);
        $('#mydata').html(table)
        $('#total').html(Math.round(total,2))
         $('#totalamount').html(maintotal)
       
       
      }
      
    });
    if(year !='a' && month !="a" && cat !='b'){
        $('#year-month').hide()
        $('#subcategry').show()
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
                if(alldata[x].amount>0){
                total+=alldata[x].amount;
                table+=`
                  <tr>
                    <td>${m}-${d}-${y}</td>
                    <td>${alldata[x].Sub}</td>
                    <td>${alldata[x].amount}</td>
                   
                  </tr>
                `;
                }
                else{
                  rufundamount+=alldata[x].amount
                }
              }
              let maintotal=total+(rufundamount)
            
              $('#subdata').html(table)
              $('#subtotal').html(Math.round(total,2))
               $('#totalamount').html(maintotal)
              
            
            }
          });
        
      
        //code end
        $('#subdata').empty()
        $('#subtotal').empty()
         $('#totalamount').empty()
    
    }
    monthlyreport=null;
    $('#monthlydata').empty();
    $('#mydata').empty()
    $('#total').empty()
  }

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
    
    // maintotal=subtotal+(total)
  
  }
});

$('#rmydata').empty()
$('#rtotal').empty()
// MY FUNCTION END 

}

// function refund end