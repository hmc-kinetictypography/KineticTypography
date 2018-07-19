//
//  SecurityQuestionViewController.swift
//  Reading Kitty
//
//  Created by cssummer18 on 6/14/18.
//  Copyright © 2018 cssummer18. All rights reserved.
//

import UIKit

class SecurityQuestionViewController: UIViewController, UITextFieldDelegate {
    /********** LOCAL VARIABLES **********/
    // Textboxes
    @IBOutlet weak var questionBox: UITextView!
    @IBOutlet weak var answerBox: UITextField!
    
    // UserDefault variables
    var securityAnswer:String = ""
    
    /********** VIEW FUNCTIONS **********/
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        // Get UserDefaults values.
        securityAnswer = UserDefaults.standard.object(forKey: "securityAnswer") as! String
        
        questionBox.text = UserDefaults.standard.object(forKey: "securityQuestion") as! String
        answerBox.delegate = self
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    
    /********** SEGUE FUNCTIONS **********/
    // When user clicks the back button, it send them to the TeacherLogin scene
    @IBAction func backButton(_ sender: Any) {
        // Go to TeacherLogin
        self.performSegue(withIdentifier: "TeacherLogin", sender: self)
    }
    
    // When user presses return, end editing
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        // submit text
        textField.resignFirstResponder()
        return true
    }
    
    // When text field is going inactive (through tabbing or returning)
    func textFieldShouldEndEditing(_ textField: UITextField) -> Bool {
        // check if answer is correct
        if textField.text == securityAnswer {
            //Go to NewPassword
            self.performSegue(withIdentifier: "NewPassword", sender: self)
        }
        return true
    }

//    // Passing data
//    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
//        //UserDefaults.standard.set(modelController, forKey: "modelController")
//
//        // Update the modelController in TeacherLogin
//        if segue.destination is TeacherLoginViewController {
//            let Destination = segue.destination as? TeacherLoginViewController
//            Destination?.modelController = modelController
//        }
//
//        // Update the modelController in NewPassword
//        if segue.destination is NewPasswordViewController {
//            let Destination = segue.destination as? NewPasswordViewController
//            Destination?.modelController = modelController
//        }
//    }
}
