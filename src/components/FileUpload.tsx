import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X } from 'lucide-react';
import { motion } from 'framer-motion';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  selectedFile?: File;
  onFileRemove?: () => void;
  accept?: string;
  maxSize?: number;
  disabled?: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  selectedFile,
  onFileRemove,
  accept = '.csv,.xlsx,.xls',
  maxSize = 10 * 1024 * 1024, // 10MB
  disabled = false,
}) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
    },
    maxSize,
    multiple: false,
    disabled,
  });

  if (selectedFile) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="card"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-primary-100 rounded-lg">
              <File className="h-5 w-5 text-primary-600" />
            </div>
            <div>
              <p className="font-medium text-gray-900">{selectedFile.name}</p>
              <p className="text-sm text-gray-500">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
          {onFileRemove && (
            <button
              onClick={onFileRemove}
              className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          )}
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      {...getRootProps()}
      className={`card cursor-pointer transition-all duration-200 ${
        isDragActive 
          ? 'border-primary-400 bg-primary-50 shadow-lg' 
          : 'border-dashed border-2 border-gray-300 hover:border-primary-400 hover:bg-primary-50'
      } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      whileHover={!disabled ? { scale: 1.02 } : {}}
      whileTap={!disabled ? { scale: 0.98 } : {}}
    >
      <input {...getInputProps()} />
      <div className="text-center py-8">
        <Upload className={`mx-auto h-12 w-12 mb-4 ${
          isDragActive ? 'text-primary-600' : 'text-gray-400'
        }`} />
        <p className="text-lg font-medium text-gray-900 mb-2">
          {isDragActive ? 'Drop your file here' : 'Upload your data file'}
        </p>
        <p className="text-sm text-gray-500 mb-4">
          Drag and drop or click to select CSV or Excel files
        </p>
        <div className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
          <Upload className="h-4 w-4 mr-2" />
          Choose File
        </div>
        <p className="text-xs text-gray-400 mt-3">
          Maximum file size: {maxSize / 1024 / 1024}MB
        </p>
      </div>
    </motion.div>
  );
};

export default FileUpload;