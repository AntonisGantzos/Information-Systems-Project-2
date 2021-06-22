# 2η Υποχρεωτική Εργασία Πληροφοριακών Συστημάτων 

## Πανεπιστήμιο Πειραιώς

## Ονοματεπώνυμο : Αντώνης Γάντζος

## ΑΜ : E18030

Σκοπός της εργασίας της οποίας εκπονήσαμε είναι ο υλοποίηση μίας Διαδυκτιακής εφαρμογής για ένα Super-Market, που θα αλληλοεπιδράει με μία βάση Δεδομένων (DSMarkets) και θα αποθηκεύει εγγραφές χρηστών και προϊόντων. Η Βάση Δεδομένων μας θα αποτελείται από 2 collections, το collection <ins>Users</ins>, όπου θα αποθηκεύουμε τα στοιχεία των Χρηστών και το collection <ins>Products</ins>, όπου θα αποθηκεύουμε τα στοιχεία και τα χαρακτηριστικά των προϊόντων. Οι χρήστες που θα αποθηκεύουμε χωρίζονται σε απλούς χρήστες (users) και διαχειριστές (admins). Η εφαρμογή αποτελείται συνολικά από 13 endpoints, τα οποία αναπαριστώνται στο κώδικα με τη μορφή συναρτήσεων.  

**Create User (1ο Endpoint)** :   Ένας απλός χρήστης δίνει τα στοιχεία του (όνομα, κωδικός και email) και εισάγεται στο Collection Users, αν δεν προ-υπάρχει ήδη. Επίσης ενημερώνουμε τη ΒΔ ότι η εισαγωγή πρόκειται για έναν απλό χρήστη ορίζοντας το σε ένα πεδίο που ονομάζουμε category. Σε περίπτωση που ο χρήστης δεν έχει δώσει τα κατάλληλα στοιχεία ή προ-υπάρχει ήδη στη ΒΔ, το πρόγραμμα στέλνει ένα κατάλληλο μήνυμα. Χρησιμοποιούμε τη μέθοδο POST, επειδή κάνουμε εισαγωγή στοιχείων στη βάση δεδομένων.

**Create Admin (2ο Endpoint)** :   Ένας διαχειριστής δίνει τα στοιχεία του (όνομα, κωδικός και email) και εισάγεται στο Collection Users, αν δεν προ-υπάρχει ήδη. Επίσης ενημερώνουμε τη ΒΔ ότι η εισαγωγή πρόκειται διαχειριστή ορίζοντας το σε ένα πεδίο που ονομάζουμε category. Ξεχωρίζουμε τις κατηγορίες χρηστών καθώς ο διαχειριστής έχει πρόσβαση σε μερικά endpoints στα οποία ο χρήστης δεν έχει. Σε περίπτωση που ο χρήστης-διαχειριστής δεν έχει δώσει τα κατάλληλα στοιχεία ή προ-υπάρχει ήδη στη ΒΔ, το πρόγραμμα στέλνει ένα κατάλληλο μήνυμα. Χρησιμοποιούμε τη μέθοδο POST, επειδή κάνουμε εισαγωγή στοιχείων στη βάση δεδομένων.

**Login (3ο Endpoint)** : Αυθεντικοποίηση των στοιχείων του χρήστη. Ο χρήστης καλείται να δώσει το email του (μοναδικό για κάθε χρήστη) και τον κωδικό του και το πρόγραμμα ελέγχει αν τα στοιχεία βρίσκονται στο collection Users. Αν υπάρχουν αυθεντικοποιεί τον χρήστη, αλλιώς στέλνει το κατάλληλο μήνυμα. Κατάλληλο μήνυμα στέλνεται και στη περίπτωση που ο χρήστης δεν έχει στείλει τα σωστά στοιχεία ή τα στοιχεία που έχει στείλει είναι ελλειπή. 

**Get Product(4ο Endpoint)** : Αναζήτηση προϊόντος στο collection Products αφού γίνει η αυθεντικοίηση του χρήστη. Ο χρήστης δίνει το όνομα ή το μοναδικό id ή τη κατηγορία του προϊόντος που επιθυμεί να ψάξει. Αν υπάρχουν παραπάνω από ένα ίδια προϊόντα εμφανίζονται στον χρήστη ταξινομημένα, ανάλογα με το κλειδί αναζήτησης που χρησιμοποίησε (σε περίπτωση που το search key είναι το όνομα του προϊόντος τα αποτελέσματα εμφανίζονται ταξινομημένα σε αλφαβητική σειρά και σε περίπτωση που το search key ήταν η κατηγορία του προϊόντος εμφανίζονται ταξινομημένα ανάλογα με τις τιμές τους σε αύξουσα σειρά). Αν ο χρήστης δεν είνα αυθεντικοποιημένος εμφανίζεται το κατάλληλο μήνυμα και το endpoint σταματά. Χρησιμοποιούμε τη μέθοδο GET, επειδιώκουμε να κάνουμε access μία εγγραφή από τη βάση δεδομένων.

**Add Product to Cart (5ο Endpoint)**: Προσθήκη προϊόντος στο καλάθι (UserCart global dictionary) και αυθεντικοποίηση του χρήστη. Ο χρήστης μπορεί να αναζητήσει το προϊόν με βάση τον μοναδικό κωδικό του (id). Επίσης ο χρήστης καλείται να δώσει και το email του για να προσθεθεί η παραγγελία του στο ιστορικό παραγγελιών του. Ακόμα, ανάλογα με τα προϊόντα που προσθέτει ο χρήστης υπολογίζεται και το συνολικό κόστος της παραγγελίας και το προσθέτουμε και αυτό το καλάθι.Αν ο χρήστης δεν είνα αυθεντικοποιημένος εμφανίζεται το κατάλληλο μήνυμα και το endpoint σταματά. Χρησιμοποιούμε τη μέθοδο GET, επειδιώκουμε να κάνουμε access μία εγγραφή από τη βάση δεδομένων.

**Show Cart (6o Endpoint)** : Γίνεται αυθεντικοποίηση του χρήστη και εμφανίζεται το μέχρι τώρα καλάθι του. Αν ο χρήστης δεν είνα αυθεντικοποιημένος εμφανίζεται το κατάλληλο μήνυμα και το endpoint σταματά. Χρησιμοποιούμε τη μέθοδο GET, επειδιώκουμε να κάνουμε access μία εγγραφή από τη βάση δεδομένων.

**Delete from Cart (7ο Endpoint)** : Αυθεντικοποίηση του χρήστη και διαγραφή του προϊόντος που θα επιλέξει με βάση το μοναδικό κωδικό του (_id). Το κόστος μειώνεται ανάλογα με τη τιμή του προϊόντος που διαγράφεται από το καλάθι. Αν ο χρήστης δεν είνα αυθεντικοποιημένος εμφανίζεται το κατάλληλο μήνυμα και το endpoint σταματά. Χρησιμοποιούμε τη μέθοδο GET, επειδιώκουμε να κάνουμε access μία εγγραφή από τη βάση δεδομένων.

**Checkout (8o Endpoint)** : Αυθεντικοποίηση του χρήστη και πληρωμή του συνολικού κόστους του καλαθιού που υπολογίζουμε στο 6ο και 7ο endpoint, ανάλογα με τις καταχωρήσεις του χρήστη στο καλάθι μέχρι τώρα. Για να γίνει η πληρωμή ο χρήστης καλείται να δώσει έναν 16-ψηφιο αριθμό (γίνεται έλεγχος για το μήκος των ψηφίων του αριθμού. Αν ο αριθμός δεν είναι 16-ψήφιος εμφανίζεται το κατάλληλο μήνυμα στον χρήστη). Στο τέλος του endpoint το καλάθι αδειάζει.Αν ο χρήστης δεν είνα αυθεντικοποιημένος εμφανίζεται το κατάλληλο μήνυμα και το endpoint σταματά. Χρησιμοποιούμε τη μέθοδο GET, επειδιώκουμε να κάνουμε access μία εγγραφή από τη βάση δεδομένων.

**Show Order History (9o Endpoint)** : Γίνεται αυθεντικοποίηση του χρήστη και εμφανίζεται το ιστορικό παραγγελιών με βάση όσα έχει προσθέσει ως τώρα στο καλάθι του. Αν ο χρήστης δεν είνα αυθεντικοποιημένος εμφανίζεται το κατάλληλο μήνυμα και το endpoint σταματά. Χρησιμοποιούμε τη μέθοδο GET, επειδιώκουμε να κάνουμε access μία εγγραφή από τη βάση δεδομένων.

**Delete User (10o Endpoint)** : Γίνεται αυθεντικοποίηση του χρήστη και έχει τη δυνατότητα να αφεραίσει κάποιον χρήστη από το collection users, δηλαδή τη συλλογή με τους εγγεγραμμένους χρήστες στην εφαρμογή του Super Market με βάση το μοναδικό email του χρήστη. Αν ο χρήστης δεν είνα αυθεντικοποιημένος εμφανίζεται το κατάλληλο μήνυμα και το endpoint σταματά. Χρησιμοποιούμε τη μέθοδο DELETE, επειδή αφαιρούμε μία εγγραφή από τη βάση δεδομένων.

**Insert Product (11ο Endpoint)**: Γίνεται έλεγχος αν ο χρήστης είναι διαχειριστής με βάση τη κατηγορία που βρίσκεται στα στοχεία του, με βάση το email του. Αν είναι έχει τη δυαντότητα να εισάγει ένα νέο προϊόν στη Βάση Δεδομένων δίνοντας τα απαραίτητα στοιχεία του προϊόντος (όνομα, κατηγορία, τιμή, περιγραφή, απόθεμα). Αν ο χρήστης δεν είναι διαχειριστής ή αν δε δωθούν τα σωστά στοιχεία για το προϊόν που θέλει να εισάγει ή αν το προϊόν προ-υπάρχει στη Βάση Δεδομένων, εμφανίζεται κατάλληλο μήνυμα και το endpoint σταματά. Χρησιμοποιούμε τη μέθοδο POST, επειδή κάνουμε εισαγωγή στοιχείων στη βάση δεδομένων.

**Delete Product (12ο Endpoint)**: Γίνεται έλεγχος αν ο χρήστης είναι διαχειριστής με βάση τη κατηγορία που βρίσκεται στα στοχεία του, με βάση το email του. Αν είναι έχει τη δυαντότητα να διαγράψει ένα προϊόν στη Βάση Δεδομένων δίνοντας τον μοναδικό κωδικό του  προϊόντος. Αν ο χρήστης δεν είναι διαχειριστής ή αν το  προϊόν που επιθυμεί να διαγράψει δεν υπάρχει στη Βάση Δεδομένων, εμφανίζεται κατάλληλο μήνυμα και το endpoint σταματά. Χρησιμοποιούμε τη μέθοδο DELETE, επειδή αφαιρούμε μία εγγραφή από τη βάση δεδομένων.

**Update Product (13ο Endpoint)**: Γίνεται έλεγχος αν ο χρήστης είναι διαχειριστής με βάση τη κατηγορία που βρίσκεται στα στοχεία του, με βάση το email του. Αν είναι έχει τη δυαντότητα να ενημερώσε ένα προϊόν στη Βάση Δεδομένων δίνοντας τον μοναδικό κωδικό του  προϊόντος. Ο διαχειριστής θα έχει τη δυνατότητα να ενημερώσει μία ή περισσότερες από τις εξής κατηγορίες (name, category, price, description). Αν ο χρήστης δεν είναι διαχειριστής ή αν το  προϊόν που επιθυμεί να διαγράψει δεν υπάρχει στη Βάση Δεδομένων, εμφανίζεται κατάλληλο μήνυμα και το endpoint σταματά. Χρησιμοποιούμε τη μέθοδο Patch, επειδή κάνουμε ενημέρωση της βάσης δεδομένων

Για να τρέξει την εφαρμογή ο χρήστης θα χρειαστεί αρχικά να τρέξει τον κώδικα σε ένα τερματικό. Ακόμα θα χρειαστεί να δημιουργήσει ένα docker container, που θα περιλαμβάνει τα images των mongo, ώστε να μπορεί να δημιουργήσει και να επεξεργαστεί τη Βάση Δεδομένων του και του web service Flask, με το οποίο δημιουργούμε τα **app_routes** της ιστοσελίδας μας. Με τα app_routes ορίζουμε τα διαφορετικά urls και κατά συνέπεια τις διαφορετικές λειτουργίες που θα έχει η εφαρμογή μας. Ορίζουμε κάθε endpoint σε ένα αντίστοιχο app_route για να εμφανίζεται με τη μορφή υπο-καταλόγου της ιστοσελίδας . Αυτό έχει τη δυνατότητα να το κάνει προσθέτοντας τα 2 images σε ένα Dockerfile μαζί με τα δεδομένα και τo python script της εφαρμογής και χρησιμοποιώντας την εντολή <ins>docker . build</ins> , ώστε να δημιουργήσει το container που θα περιλαμβάνει τα 2 images. Η τελεία ορίζει στο τερματικό να δημιουργήσει μία εικόνα με βάση το Dockerfile που βρίσκεται στον τρέχων κατάλογό μας. Για να τρέξουν και τα 2 images ταυτόχρονα χρησιμοποιούμε ένα αρχείο docker-compose. Για να τρέξουμε το docker-compose χρησιμοποιούμε την εντολή <ins>docker-compose up</ins> στο τερματικό μας.  Επίσης για δοκιμές της εγκυρότητας του κώδικα που αναπτύξαμε για την εργασία χρησιμοποιούμε το εργαλείο Postman. Για την υλοποίηση της Βάσης Δεδομένων εργαζόμαστε ως εξής. Εφόσον έχουμε δημιουργήσει με επιτυχία το mongo container (ενδεικτικά το έχουμε ονομάσει mongodb) χρησιμοποιούμε την εντολή <ins>docker exec -it mongodb mongo</ins> , ώστε να αποκτήσουμε πρόσβαση στο mongo shell. Εκεί χρησιμοποιούμε την εντολή use DSMarkets(το όνομα της Βάσης Δεδομένων μας). Η εντολή αυτή μας δίνει πρόσβαση στη Βάση Δεδομένων του συστήματος που επιθυμούμε και αν η βάση δεν υπάρχει, την δημιουργεί. Αφού δημιουργήσουμε τη βάση φτιάχνουμε τα Collections, τις συλλογές όπου θα αποθηκεύουμε τα στοιχεία χρηστών και προϊόντων. Για αυτό υλοποιούμε 2 collections, μία για τους χρήστες(ονομάζουμε ενδεκτικά Users) και μία για τα προϊόντα(την ονομάζουμε ενδεικτικά Products). Για τη κατασκευή των collections χρησιμοποιούμε την εντολή <ins>db.createCollection("ονομα Collection")</ins>, κι αφού βρισκόμαστε μέσα στη db DSMarket που δημιουργήσαμε νωρίτερα, τα 2 collections δημιουργούνται μέσα σε αυτή.
