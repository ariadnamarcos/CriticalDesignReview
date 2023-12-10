<?php
include("db.php"); //include aplica el codi de l'arxiu que dius, aquest obre la db

//https://localhost:8080/CriticalDesignPBE/back/index.php/timetables?day=FRi&hour=8:00&subject=PBE 

function parse_query($query){   //fa una llista key-value separant per =
    foreach($query as $val){
        list($key, $value) = explode('=', $val);
        $params[$key] = $value;
    }
    return $params;
}
$table = ltrim($_SERVER['PATH_INFO'], '/'); //s'ha de treure el '/' davant de la taula
if($table == 'students'){
    $consulta = "SELECT userName FROM {$table}";
}else{
    $consulta = "SELECT * FROM {$table}";  
}
if($_SERVER['QUERY_STRING'] != NULL){
    $query = explode('&', $_SERVER['QUERY_STRING']); //quedarà un array [day=Fri, hour=8:00, subject=PBE]

    $params = parse_query($query);  //Array ( [day] => FRi, [hour] => 8:00, [subject] => PBE )
    $primeraCondicio = true;
    foreach($params as $key => $value){
        if(isset($key)){
            $consulta .= ($primeraCondicio ? " WHERE" : " AND");  //tria WHERE si &primeraciondició=True
            $primeraCondicio = false;  
 
            $keyParts = explode('[', $key);     //en aquesta secció de codi es on posem les codicións lt and gt
            if (isset($keyParts[1])) {
                $cond = trim($keyParts[1],']');
                if($cond =='gt'){
                    $simb ='>';
                }else if ($cond =='lt'){
                    $simb ='<';
                }                               //si volem posar mes condicionants només hem d'afegir else if
            }else{
                $simb ='=';
            }
            $key = $keyParts[0];
            $consulta .=" $key $simb '$value'";

            }
    }
    
}

if ($table == 'marks' && isset($params['uid'])) {
	$consulta .= " AND uid = '{$params['uid']}'";
}
if ($table == 'marks'){
	$consulta .= " ORDER BY subject ASC";
}
if($table == 'tasks'){
	$consulta .= " ORDER BY date ASC";
}


$dia = date('N');
$hora_actual = date('H:i:s');
$days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
$days_inorder = array_merge(
    array_slice($days, $dia), 
    array_slice($days, 0, $dia)  
);
$hora_str = strval($hora_actual);
$order_clause = implode(',', array_map(function ($day) {
    return "'$day'";
}, $days_inorder));

if ($table == 'timetables') {
	if(($dia >= 1) && ($dia <= 5)){	//si es entre setmana
		$dia = (date('N') + 1)%7;	//per aquesta solucio primer s'agafa el dia actual i les hores de despres de la actual i 
						//despres ordenem cronologicament com si fos el dia seguent a l'actual
		$consulta .= " ORDER BY CASE WHEN (day = '$days[$dia]' && hour > '$hora_str') THEN 0 ELSE 1 END, FIELD(day, $order_clause), hour";
	}else{ // si es cap de setmana simplement donem l'horari normal
		$consulta .= " ORDER BY FIELD(day, $order_clause), hour";
	}
}

$result = mysqli_query($conn, $consulta);  //executa la consulta $consulta a la db $conn
$data= array(); //l'inicialitzem com un array buit
while($row = mysqli_fetch_assoc($result)){  //anem recollint els arrays de les diferents columnes i fent un array de arrays, és a dir, una matriu
    $data[] = $row;
}
header('Content-Type: application/json');  //indiquem a la capçalera que les dades son en foramt json
echo json_encode($data);    //les enviem al client codificades en aquest format
?>
