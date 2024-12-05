package Previous_Version;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.io.BufferedWriter;
import java.io.FileWriter;

public class readFile {

    public readFile() {
        // Default constructor
    }

    public ArrayList<Photo> read(String path) {
        ArrayList<Photo> result = new ArrayList<>(); // To store the parsed data
        int counter = 0;
        
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            String line = reader.readLine(); // Read the first line (number of entries, can be ignored)
            int count = Integer.parseInt(line); // Parse the number of entries (for validation)
            
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(" ", 3); // Split into type, count, and tags
                String type = parts[0]; // "H" or "V"
                String tags = parts[2]; // The rest are tags
                String[] tag = tags.split(" ");
                
                result.add(new Photo("Photo" + counter, type, tag));
                counter++;
            }

            // Ensure the number of entries matches the count in the file
            if (result.size() != count) {
                throw new IOException("Mismatch between stated and actual number of entries.");
            }

            
        } catch (IOException e) {
            e.printStackTrace();
        }

        return result;
    }

    public void writeFile(ArrayList<Score> result){
        try(BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt"))){
            writer.write(result.size() + 1  + "\n");
            for(int i = 0 ; i < result.size() ; i++){
                if(i == 0){
                    writer.write(result.get(i).getPhoto1().getName() + "\n");
                    writer.write(result.get(i).getPhoto2().getName() + "\n");
                }
                else{
                    if(result.get(i).getPhoto2() == null){
                        continue;
                    }
                    else{
                        writer.write(result.get(i).getPhoto2().getName() +  "\n");
                    }
                }
            }
        }catch(IOException e){
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        readFile rf = new readFile();
        String filePath = "input.txt";
        ArrayList<Photo> data = rf.read(filePath);

        for (Photo photo : data) {
            System.out.println("Name: " + photo.getName());
            System.out.println("Type: " + photo.getType());
            System.out.print("Tags: ");
            for (String tag : photo.getTags()) {
                System.out.print(tag + " ");
            }
            System.out.println();
            System.out.println("Used: " + photo.getUsed());
            System.out.println();
        }
    }
}
