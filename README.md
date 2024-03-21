### Airline reservation system

An airline reservation system implemented in Python using Flask for the backend and MongoDB for data storage. It allows users to register, log in, search for flights, make reservations, and view reservations. Administrative functionalities include adding, deleting, and updating flights. The project is containerized using Docker for easy deployment and management.

---
### Τρόπος λειτουργίας

Δημιουργία ενός docker image που συνδέεται με ένα container της MongoDB , εισαγωγή της βάσης δεδομένων DSAirlines που περιέχει τα collections "Users" , "Flights", "Reservations" στο image.
Εκκίνηση του Docker Image , εισαγωγή του κώδικα στο Visual Studio με την ονομασία air.py εκκίνηση του κώδικα με την επιλογή Flask.
Για την δοκιμή ανοίγουμε το postman και δημιουργούμε το request που επιθυμούμε να δοκιμάσουμε εισάγοντας στο url  http://192.168.2.4:5000/ + το @app route του function. πχ. για το create_simple_user  http://192.168.2.4:5000/create_simple_user. Έπειτα, πατώντας body εισάγουμε στην επιλογή raw τις πληροφορίες σε μορφή json.




## Δημιουργία απλού χρήστη - def create_simple_user()
Γίνεται έλεγχος εάν το email ή username που έδωσε ο χρήστης, καθώς και το passport εάν υπάρχουν ήδη στη βάση. Εάν δεν υπάρχουν τότε γίνεται έλεγχος του password. Θα πρέπει να αποτελείται από 8 χαρακτήρες από τους οποίους ο ένας τουλάχιστον να είναι αριθμός. Εφόσον τα στοιχεία πληρούν τα κριτήρια, γίνεται η δημιουργία του χρήστη και σε αντίθετη περίπτωση εμφανίζονται κατάλληλα μηνύματα. Το user_category παίρνει αντίστοιχη τιμή και με αυτή την μεταβλητή ο user θα έχει πρόσβαση σε ορισμένες λειτουργίες. 


## Είσοδος στο σύστημα - login()
Γίνεται έλεγχος εάν το email ή username που έδωσε ο χρήστης υπάρχουν στη βάση και στη συνέχεια γίνεται έλεγχος και αν ο κωδικός που έδωσε είναι ο σωστός. Εφόσον τα στοιχεία πληρούν τα κριτήρια, δημιουργείται ένα global user_category, με το οποίο καταλαβαίνει αυτόματα το σύστημα το είδος του χρήστη σε όλες τις functions, και ένα global currentUser, όπου αποθηκεύει το όνομα του χρήστη, δηλαδή ο χρήστης δεν χρειάζεται να ξανά δώσει ως τιμή το όνομα του για να ενεργοποιήσει την sortDescending().

## Αναζήτηση πτήσης – search()
Ο χρήστης δίνοντας την τοποθεσία του, τον επιθυμητό προορισμό και την ημερομηνία αναχώρησης, αναζητεί πτήσεις. Αρχικά, γίνεται έλεγχος για το εάν υπάρχουν πτήσεις με αυτά τα δεδομένα και εάν υπάρχουν διαθέσιμα εισιτήρια. Εφόσον τα στοιχεία πληρούν τα κριτήρια,  εμφανίζεται λεπτομερώς η αντίστοιχη πτήση.

## Κράτηση εισιτηρίου - reservation()
Ο χρήστης δίνει τα στοιχεία του και γίνεται έλεγχος εάν η κάρτα που έδωσε έχει 16 ψηφία. Εφόσον τα στοιχεία πληρούν τα κριτήρια,  γίνεται η κράτηση του εισιτηρίου, μειώνεται η διαθεσιμότητα της πτήσεις κατά ένα και εμφανίζονται τα στοιχεία της κράτησης.

## Εμφάνιση υπάρχουσας κράτησης - showReservation()
Δίνεται ως είσοδος ο μοναδικός κωδικός της κράτησης και επιστρέφονται τα στοιχεία της.

## Ακύρωση κράτησης – deleteReservation()
Δίνεται ως είσοδος ο μοναδικός κωδικός της κράτησης, η κράτηση διαγράφεται και επιστέφεται μήνυμα ότι τα χρήματα επιστράφηκαν στην κάρτα του χρήστη και ο αριθμός της κάρτας.

## Εμφάνιση όλων των κρατήσεων βάση προορισμού – searchDestination()
Ο χρήστης δίνει έναν προορισμό και εμφανίζονται τα στοιχεία τις κράτησης με αυτόν τον προορισμό. ( συγκρίνει τα  flight_id του flight και του reservation και έτσι μπορεί να βρει τα στοιχεία της κράτησης. 

## Εμφάνιση όλων των κρατήσεων με χρονολογική σειρά – sortDescending()
Ο χρήστης μπορεί να ταξινομήσει τις κρατήσεις του με χρονολογική σειρά. Δίνοντας ως είσοδο 0 ( {  "choice": "0"} ),  ο χρήστης τα ταξινομεί με DESCENDING, δίνοντας άλλο τιμή ο χρήστης τα ταξινομεί με ASCENDING. Με όποιο τρόπο ταξινόμησης επιλέξει ο χρήστης, επιστρέφονται οι κρατήσεις ταξινομημένες. 

##  Εισαγωγή νέου διαχειριστή – create_admin()
Γίνεται έλεγχος τα στοιχεία του χρήστη για το εάν υπάρχουν ήδη στο σύστημα. Εάν δεν υπάρχουν τότε δημιουργείται ο χρήστης. Το user_category παίρνει αντίστοιχη τιμή και με αυτή την μεταβλητή ο admin θα έχει πρόσβαση σε ορισμένες λειτουργίες. 

## Δημιουργία πτήσης – addFlight()
Ο διαχειριστής δίνει τα απαραίτητα στοιχεία της πτήσης και εφόσον δεν λείπει κάποιο στοιχείο, δημιουργείται η πτήση.

## Διαγραφή πτήσης – deleteFlight()
Ο διαχειριστής δίνει τον μοναδικό κωδικό πτήσης και να την αναζητήσεις. Εάν η πτήση βρεθεί τότε διαγράφεται.

## Αλλαγή τιμής πτήσης – updateFlight()
 Αρχικά, ο διαχειριστής δίνει τον μοναδικό κωδικό της πτήσης και την νέα τιμή της. Στην συνέχεια, γίνεται έλεγχος για το εάν η νέα τιμή είναι αποδεκτή, εάν δεν έχει κάνει κάποιος κράτηση (έχει, δηλαδή, 220 θέσεις) και ο κωδικός που βρέθηκε είναι σωστός. Εφόσον ο κωδικός πληροί τα κριτήρια, τότε γίνεται η αλλαγή.

